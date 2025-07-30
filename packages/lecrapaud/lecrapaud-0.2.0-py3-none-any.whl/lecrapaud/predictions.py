import keras
import pickle
import pandas as pd
from pathlib import Path
import joblib
from datetime import timedelta, datetime
import logging

from lecrapaud.search_space import ml_models, dl_recurrent_models
from lecrapaud.data_sourcing import get_filtered_data
from lecrapaud.preprocessing import feature_engineering
from lecrapaud.feature_selection import (
    encode_categorical_features,
    reshape_df,
    TARGETS_CLF,
    reshape_time_series,
)
from lecrapaud.model_selection import predict, evaluate
from lecrapaud.utils import logger
from lecrapaud.db import Dataset
from lecrapaud.config import LOGGING_LEVEL

MODELS_LIST = ml_models + dl_recurrent_models


def run_prediction(
    dataset_id: str,
    targets_numbers: list[int],
    test: bool = True,
    date: datetime = None,
    verbose: int = 0,
):
    """Function to run prediction on several TARGETS using best models"""
    if verbose == 0:
        logger.setLevel(logging.WARNING)

    logger.warning("Running prediction...")

    dataset = Dataset.get(dataset_id)
    dataset_dir = dataset.path
    preprocessing_dir = f"{dataset_dir}/preprocessing"
    list_of_groups = dataset.list_of_groups

    features_dict = {}
    scaler_y_dict = {}
    model_dict = {}
    threshold_dict = {}
    for target_number in targets_numbers:
        (
            model_dict[target_number],
            threshold_dict[target_number],
            features_dict[target_number],
            scaler_y_dict[target_number],
            all_features,
            scaler_x,
        ) = load_model(dataset, target_number)

    # get data for backtesting
    if test:
        train_data_dir = f"{dataset_dir}/data"
        data_for_pred = joblib.load(f"{train_data_dir}/test.pkl")
        data_for_pred_scaled = joblib.load(f"{train_data_dir}/test_scaled.pkl")

        if any(
            config["recurrent"]
            for config in MODELS_LIST
            if config["model_name"] in model_dict.values()
        ):
            train_scaled = joblib.load(f"{train_data_dir}/train_scaled.pkl")
            val_scaled = joblib.load(f"{train_data_dir}/val_scaled.pkl")
            test_scaled = joblib.load(f"{train_data_dir}/test_scaled.pkl")
            reshaped_data = reshape_time_series(
                train_scaled, val_scaled, test_scaled, all_features, timesteps=120
            )
            data_for_pred_reshaped = reshaped_data["x_train_reshaped"]

        most_recent_data = joblib.load(f"{train_data_dir}/full.pkl")
        most_recent_data = most_recent_data.loc[data_for_pred.index]

        scores_clf = []
        scores_reg = []
    # get data for predicting future
    else:
        # TODO: if date is a bit more older, need more than 0 years
        most_recent_data = get_filtered_data(
            years_of_data=0, list_of_groups=list_of_groups
        )

        most_recent_data = feature_engineering(
            most_recent_data, for_training=False, save_as_csv=True
        )

        data_for_pred = encode_categorical_features(
            most_recent_data, save_dir=preprocessing_dir, fit=False
        )

        data_for_pred_scaled = pd.DataFrame(
            scaler_x.transform(data_for_pred[all_features]),
            columns=list(data_for_pred[all_features].columns),
            index=data_for_pred.index,
        )

        # TODO: don't we need to have 120 days of data for each stock?
        if any(
            config["recurrent"]
            for config in MODELS_LIST
            if config["model_name"] in model_dict.values()
        ):
            # Count number of rows per stock
            counts = data_for_pred["STOCK"].value_counts()

            # Find stocks with insufficient history
            insufficient_stocks = counts[counts < 120]

            if not insufficient_stocks.empty:
                raise ValueError(
                    f"Insufficient history for stocks: {', '.join(insufficient_stocks.index)}"
                )

            data_for_pred_reshaped = reshape_df(
                data_for_pred_scaled[all_features], data_for_pred["STOCK"], 120
            )

    # make prediction
    for target_number in targets_numbers:

        # Prepare variables and data
        target_type = "classification" if target_number in TARGETS_CLF else "regression"
        features = features_dict[target_number]
        model = model_dict[target_number]
        threshold = threshold_dict[target_number]

        config = [
            config for config in MODELS_LIST if config["model_name"] == model.model_name
        ]
        if config is None or len(config) == 0:
            Exception(f"Model {model.model_name} was not found in search space.")
        else:
            config = config[0]

        need_scaling = config["need_scaling"] and target_type == "regression"
        if config["recurrent"]:
            features_idx = [i for i, e in enumerate(all_features) if e in set(features)]
            x_pred = data_for_pred_reshaped[:, :, features_idx]
        else:
            x_pred = (
                data_for_pred_scaled[features]
                if need_scaling
                else data_for_pred[features]
            )

        # Predict
        y_pred = predict(model, x_pred, target_type, config, threshold)

        # Fix for recurrent model because x_val has no index as it is a 3D np array
        if config["recurrent"]:
            y_pred.index = (
                most_recent_data.index
            )  # TODO: not sure this will work for old dataset not aligned with data_for_training for test use case (done, this is why we decode the test set)

        # Unscale prediction
        if need_scaling or config["recurrent"]:
            scaler_y = scaler_y_dict[target_number]
            y_pred = pd.Series(
                scaler_y.inverse_transform(y_pred.values.reshape(-1, 1)).flatten(),
                index=most_recent_data.index,
            )
            y_pred.name = "PRED"

        # Evaluate if test
        if test:
            prediction = pd.concat(
                [most_recent_data[f"TARGET_{target_number}"], y_pred], axis=1
            )
            prediction.rename(
                columns={f"TARGET_{target_number}": "TARGET"}, inplace=True
            )
            score = evaluate(prediction, target_type)
            score["TARGET"] = f"TARGET_{target_number}"
            (
                scores_clf.append(score)
                if target_type == "classification"
                else scores_reg.append(score)
            )

        if isinstance(y_pred, pd.DataFrame):
            y_pred.rename(
                columns={"PRED": f"TARGET_{target_number}_PRED"}, inplace=True
            )
            most_recent_data = pd.concat(
                [most_recent_data, y_pred[f"TARGET_{target_number}_PRED"]], axis=1
            )

        else:
            y_pred.name = f"TARGET_{target_number}_PRED"
            most_recent_data = pd.concat([most_recent_data, y_pred], axis=1)

    # return result either for test set or for tomorrow prediction
    result = most_recent_data

    if verbose == 0:
        logger.setLevel(LOGGING_LEVEL)

    if test:
        logger.info("Test results on test set")
        scores_reg = pd.DataFrame(scores_reg).set_index("TARGET")
        scores_clf = pd.DataFrame(scores_clf).set_index("TARGET")
        return result, scores_reg, scores_clf, prediction
    elif date:
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = date + timedelta(days=1)
        logger.info(f"Prediction for : {tomorrow.date()}")
        result = result[result["DATE"] == date]
        return result, None, None, None
    else:
        date = datetime.today()
        max_date = result["DATE"].max()
        if max_date.date() != date.date():
            logger.info(
                f"The maximum date found in the dataset is {max_date} and not {date}"
            )
        tomorrow = max_date + timedelta(days=1)
        logger.info(f"Prediction for tomorrow : {tomorrow.date()}")

        # Filter the DataFrame for the last date
        filtered_result = result[result["DATE"] == max_date]

        return filtered_result, None, None, None


# Helpers
def load_model(dataset: Dataset, target_number: int):
    dataset_dir = dataset.path
    training_target_dir = f"{dataset_dir}/TARGET_{target_number}"
    preprocessing_dir = f"{dataset_dir}/preprocessing"

    # Search for files that contain '.best' or '.keras' in the name
    scores_tracking = pd.read_csv(f"{training_target_dir}/scores_tracking.csv")
    training_target_dir = Path(training_target_dir)
    best_files = list(training_target_dir.glob("*.best*")) + list(
        training_target_dir.glob("*.keras*")
    )
    threshold = (
        scores_tracking["THRESHOLD"].values[0]
        if "THRESHOLD" in scores_tracking.columns
        else None
    )

    # If any files are found, try loading the first one (or process as needed)
    if best_files:
        file_path = best_files[0]  # Assuming you want to open the first matching file
        try:
            # Attempt to load the file as a scikit-learn, XGBoost, or LightGBM model (Pickle format)
            model = joblib.load(file_path)
            logger.info(f"Loaded model {model.model_name} and threshold {threshold}")
        except (pickle.UnpicklingError, EOFError):
            # If it's not a pickle file, try loading it as a Keras model
            try:
                # Attempt to load the file as a Keras model
                model = keras.models.load_model(file_path)
                logger.info(
                    f"Loaded model {model.model_name} and threshold {threshold}"
                )
            except Exception as e:
                raise FileNotFoundError(
                    f"Model could not be loaded from path: {file_path}: {e}"
                )
    else:
        raise FileNotFoundError(
            f"No files with '.best' or '.keras' found in the specified folder: {training_target_dir}"
        )

    if dataset.name == "data_28_X_X":
        features = joblib.load(
            f"{preprocessing_dir}/features_{target_number}.pkl"
        )  # we keep this for backward compatibility
    else:
        features = dataset.get_features(target_number)

    scaler_y = None
    if target_number not in TARGETS_CLF:
        scaler_y = joblib.load(f"{preprocessing_dir}/scaler_y_{target_number}.pkl")

    if dataset.name == "data_28_X_X":
        all_features = joblib.load(
            f"{preprocessing_dir}/all_features.pkl"
        )  # we keep this for backward compatibility
    else:
        all_features = dataset.get_all_features()
    scaler_x = joblib.load(f"{preprocessing_dir}/scaler_x.pkl")

    return model, threshold, features, scaler_y, all_features, scaler_x
