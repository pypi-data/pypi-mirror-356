import logging
import joblib
from pathlib import Path
import os

from lecrapaud.experiment import create_dataset
from lecrapaud.feature_engineering import (
    feature_engineering,
    encode_categorical_features,
    add_pca_features,
    summarize_dataframe,
)
from lecrapaud.feature_selection import (
    feature_selection,
    train_val_test_split,
    train_val_test_split_time_series,
    scale_data,
    reshape_time_series,
)
from lecrapaud.model_selection import model_selection
from lecrapaud.search_space import all_models
from lecrapaud.directory_management import tmp_dir
from lecrapaud.db import Dataset
from lecrapaud.utils import logger
from lecrapaud.config import PYTHON_ENV


# Parameters
columns_date = ["DATE"]
columns_te_groupby = [["SECTOR", "DATE"], ["SUBINDUSTRY", "DATE"]]
columns_te_target = ["RET", "VOLUME", "RESIDUAL_RET", "RELATIVE_VOLUME"] + [
    f"{ind}_{p}"
    for p in [9, 14, 21, 50]
    for ind in [
        "CUMUL_RET",
        "SMA",
        "EMA",
        "VOLATILITY",
        "ATR",
        "ADX",
        "%K",
        "RSI",
        "MFI",
    ]
]
target_clf = [2, 4, 6, 8, 9, 10, 11]
column_ordinal = ["STOCK"]
column_binary = ["SECTOR", "SUBINDUSTRY", "LOCATION"]
columns_pca = []
target_numbers = range(1, 15)
date_column = "DATE"
group_column = "STOCK"


def run_training(
    get_data_function: function,
    get_data_params: dict = None,
    time_series: bool = False,
    dataset_id=None,
    years_of_data=2,
    list_of_groups=None,
    percentile=15,
    corr_threshold=80,
    max_features=20,
    max_timesteps=120,
    targets_numbers=range(1, 15),
    models_idx=range(len(all_models)),
    number_of_trials=20,
    perform_hyperoptimization=True,
    perform_crossval=False,
    clean_dir=False,
    preserve_model=False,
    session_name="test",
):
    logging.captureWarnings(True)

    if any(all_models[i].get("recurrent") for i in models_idx) and not time_series:
        ValueError(
            "You need to set time_series to true to use recurrent model, or remove recurrent models from models_idx chosen"
        )

    if dataset_id is None:
        # Get the data
        logger.info("Getting data...")
        data = get_data_function(**get_data_params)

        # # preprocess & feature engineering => Should be in get_data_function
        # logger.info("Preprocessing...")
        # preprocessed_data = preprocessing(data, for_training=True, save_as_csv=True)

        logger.info(f"Feature engineering for {session_name}...")
        data_for_training = feature_engineering(
            data,
            columns_date=columns_date,
            columns_te_groupby=columns_te_groupby,
            columns_te_target=columns_te_target,
        )

        # Split
        if time_series:
            train, val, test = train_val_test_split_time_series(data_for_training)
        else:
            train, val, test = train_val_test_split(
                data, stratify_col=f"target_{target_numbers[0]}"
            )  # TODO: only stratifying first target for now

        # Create Dataset / Experiment (TODO: should be defined sooner)
        dataset = create_dataset(
            train, val, test, corr_threshold, percentile, max_features
        )
        dataset_dir = dataset.path
        dataset_id = dataset.id
        data_dir = f"{dataset_dir}/data"
        preprocessing_dir = f"{dataset_dir}/preprocessing"
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(preprocessing_dir, exist_ok=True)

        # PCA
        train, pcas = add_pca_features(train, columns_pca)
        val, _ = add_pca_features(val, columns_pca, pcas=pcas)
        test, _ = add_pca_features(test, columns_pca, pcas=pcas)

        if PYTHON_ENV != "Test":
            joblib.dump(pcas, f"{preprocessing_dir}/pca.pkl")

        # Encoding
        train, transformer = encode_categorical_features(
            train, column_ordinal=column_ordinal, column_binary=column_binary
        )
        val, _ = encode_categorical_features(
            val,
            column_ordinal=column_ordinal,
            column_binary=column_binary,
            transformer=transformer,
        )
        test, _ = encode_categorical_features(
            test,
            column_ordinal=column_ordinal,
            column_binary=column_binary,
            transformer=transformer,
        )

        if PYTHON_ENV != "Test":
            joblib.dump(data_for_training, f"{data_dir}/full.pkl")
            joblib.dump(transformer, f"{preprocessing_dir}/column_transformer.pkl")
            summary = summarize_dataframe(train)
            summary.to_csv(f"{dataset_dir}/feature_summary.csv", index=False)

        # feature selection
        logger.info("Feature Selection...")
        for target_number in targets_numbers:
            feature_selection(
                dataset_id=dataset_id,
                train=train,
                target_number=target_number,
                single_process=True,
            )

        dataset = Dataset.get(dataset_id)
        all_features = dataset.get_all_features()
        columns_to_keep = all_features + [f"TARGET_{i}" for i in target_numbers]

        duplicates = [
            col for col in set(columns_to_keep) if columns_to_keep.count(col) > 1
        ]
        if duplicates:
            raise ValueError(f"Doublons détectés dans columns_to_keep: {duplicates}")

        train = train[columns_to_keep]
        val = val[columns_to_keep]
        test = test[columns_to_keep]

        # save data
        if PYTHON_ENV != "Test":
            joblib.dump(train[columns_to_keep], f"{data_dir}/train.pkl")
            joblib.dump(val[columns_to_keep], f"{data_dir}/val.pkl")
            joblib.dump(test[columns_to_keep], f"{data_dir}/test.pkl")

        # scaling features
        if any(t not in target_clf for t in target_numbers) and any(
            all_models[i].get("need_scaling") for i in models_idx
        ):
            logger.info("Scaling features...")
            train_scaled, scaler_x, scalers_y = scale_data(
                train, save_dir=preprocessing_dir
            )
            val_scaled, _, _ = scale_data(
                val, save_dir=preprocessing_dir, scaler_x=scaler_x, scalers_y=scalers_y
            )
            test_scaled, _, _ = scale_data(
                test, save_dir=preprocessing_dir, scaler_x=scaler_x, scalers_y=scalers_y
            )
        else:
            train_scaled = None
            val_scaled = None
            test_scaled = None

        # save data
        if PYTHON_ENV != "Test":
            joblib.dump(train_scaled, f"{data_dir}/train_scaled.pkl")
            joblib.dump(val_scaled, f"{data_dir}/val_scaled.pkl")
            joblib.dump(test_scaled, f"{data_dir}/test_scaled.pkl")

        data = {
            "train": train,
            "val": val,
            "test": test,
            "train_scaled": train_scaled,
            "val_scaled": val_scaled,
            "test_scaled": test_scaled,
            "scalers_y": scalers_y,
        }

    # reshape data for time series
    reshaped_data = None
    if any(all_models[i].get("recurrent") for i in models_idx) and time_series:
        # reshaping data for recurrent models
        logger.info("Reshaping data for recurrent models...")
        reshaped_data = reshape_time_series(
            train_scaled, val_scaled, test_scaled, all_features, timesteps=max_timesteps
        )

    # model selection and hyperoptimization
    logger.info("Model Selection and Hyperoptimization...")
    for target_number in target_numbers:
        model_selection(
            dataset_id=dataset_id,
            models_idx=models_idx,
            target_number=target_number,
            session_name=session_name,
            perform_hyperoptimization=perform_hyperoptimization,
            perform_crossval=perform_crossval,
            number_of_trials=number_of_trials,
            plot=False,
            clean_dir=clean_dir,
            preserve_model=preserve_model,
            reshaped_data=reshaped_data,
            data=(data or None),
        )
