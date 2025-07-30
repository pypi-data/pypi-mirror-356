import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import json
import warnings
import joblib
import glob
from pathlib import Path
import pickle

os.environ["COVERAGE_FILE"] = str(Path(".coverage").resolve())

# ML models
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    mean_absolute_percentage_error,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    roc_auc_score,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix,
)
from sklearn.preprocessing import LabelBinarizer
import lightgbm as lgb
import xgboost as xgb

# DL models
import tensorflow as tf
import keras
from keras.callbacks import EarlyStopping, TensorBoard
from keras.metrics import (
    Precision,
    Recall,
    F1Score,
)
from keras.losses import BinaryCrossentropy, CategoricalCrossentropy
from keras.optimizers import Adam

K = tf.keras.backend
from tensorboardX import SummaryWriter

# Optimization
import ray
from ray.tune import Tuner, TuneConfig, with_parameters
from ray.train import RunConfig
from ray.tune.search.hyperopt import HyperOptSearch
from ray.tune.search.bayesopt import BayesOptSearch
from ray.tune.logger import TBXLoggerCallback
from ray.tune.schedulers import ASHAScheduler
from ray.air import session

# Internal library
from lecrapaud.search_space import all_models
from lecrapaud.directory_management import clean_directory
from lecrapaud.utils import copy_any, contains_best, logger, serialize_for_json
from lecrapaud.config import PYTHON_ENV
from lecrapaud.feature_selection import load_train_data
from lecrapaud.db import (
    Model,
    ModelSelection,
    ModelTraining,
    Score,
    Target,
    Dataset,
)

# Reproducible result
keras.utils.set_random_seed(42)
np.random.seed(42)
tf.config.experimental.enable_op_determinism()


# test configuration
def test_hardware():
    devices = tf.config.list_physical_devices()
    logger.info("\nDevices: ", devices)

    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        details = tf.config.experimental.get_device_details(gpus[0])
        logger.info("GPU details: ", details)


# Suppress specific warning messages related to file system monitor
# logging.getLogger("ray").setLevel(logging.CRITICAL)
# logging.getLogger("ray.train").setLevel(logging.CRITICAL)
# logging.getLogger("ray.tune").setLevel(logging.CRITICAL)
# logging.getLogger("ray.autoscaler").setLevel(logging.CRITICAL)
# logging.getLogger("ray.raylet").setLevel(logging.CRITICAL)
# logging.getLogger("ray.monitor").setLevel(logging.CRITICAL)
# logging.getLogger("ray.dashboard").setLevel(logging.CRITICAL)
# logging.getLogger("ray.gcs_server").setLevel(logging.CRITICAL)

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class ModelEngine:

    def __init__(
        self,
        model_name: str = None,
        target_type: str = None,
        path: str = None,
        search_params: dict = {},
        create_model=None,
        plot: bool = False,
        log_dir: str = None,
    ):
        if path:
            self.load(path)
        else:
            self.model_name = model_name
            self.target_type = target_type

        config = [
            config for config in all_models if config["model_name"] == self.model_name
        ]
        if config is None or len(config) == 0:
            Exception(
                f"Model {self.model_name} is not supported by this library."
                f"Choose a model from the list of supported models: {[model['model_name'] for model in all_models].join(', ')}"
            )

        self.recurrent = config["recurrent"]
        self.need_scaling = config["need_scaling"]
        self.search_params = search_params
        self.create_model = create_model
        self.plot = plot
        self.log_dir = log_dir

        if self.need_scaling and self.target_type == "regression":
            self.scaler_y = joblib.load(f"{self.path}/scaler_y.pkl")
        else:
            self.scaler_y = None

        self.path = path

    def fit(self, *args):
        if self.recurrent:
            fit = self.fit_recurrent
        elif (self.create_model == "lgb") or (self.create_model == "xgb"):
            fit = self.fit_boosting
        else:
            fit = self.fit_sklearn
        model = fit(*args)
        return model

    # Functions to fit & evaluate models
    def fit_sklearn(self, x_train, y_train, x_val, y_val, params):

        # Create & Compile the model
        model = self.create_model(**params)

        # Train the model
        logger.info("Fitting the model...")
        logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
        logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

        model.fit(x_train, y_train)

        if (
            self.target_type == "classification"
            and "loss" in model.get_params().keys()
            and "hinge" in model.get_params()["loss"]
        ):
            # This is for SVC models with hinge loss
            # You should use CalibratedClassifierCV when you are working with classifiers that do not natively output well-calibrated probability estimates.
            # TODO: investigate if we should use calibration for random forest, gradiant boosting models, and bagging models
            logger.info(
                f"Re-Calibrating {self.model_name} to get predict probabilities..."
            )
            calibrator = CalibratedClassifierCV(model, cv="prefit", n_jobs=-1)
            model = calibrator.fit(x_train, y_train)

        # set model_name after calibrator
        model.model_name = self.model_name
        model.target_type = self.target_type

        logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")

        self._model = model

        return model

    def fit_boosting(self, x_train, y_train, x_val, y_val, params):
        """
        This is using lightGBM or XGboost C++ librairies
        """
        lightGBM = self.create_model == "lgb"

        # Datasets
        boosting_dataset = lgb.Dataset if lightGBM else xgb.DMatrix
        train_data = boosting_dataset(x_train, label=y_train)
        val_data = boosting_dataset(x_val, label=y_val)

        # Create a TensorBoardX writer
        writer = SummaryWriter(self.log_dir)
        evals_result = {}

        # Training
        labels = np.unique(y_train)
        num_class = (
            labels.size
            if self.target_type == "classification" and labels.size > 2
            else 1
        )
        logger.info("Fitting the model...")
        logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
        logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

        if lightGBM:

            def tensorboard_callback(env):
                for i, metric in enumerate(env.evaluation_result_list):
                    metric_name, _, metric_value, _ = metric
                    writer.add_scalar(
                        f"LightGBM/{metric_name}", metric_value, env.iteration
                    )

            loss = (
                "regression"
                if self.target_type == "regression"
                else ("binary" if num_class <= 2 else "multiclass")
            )
            eval_metric = (
                "rmse"
                if self.target_type == "regression"
                else ("binary_logloss" if num_class <= 2 else "multi_logloss")
            )
            model = lgb.train(
                params={
                    **params["model_params"],
                    "objective": loss,
                    "metric": eval_metric,
                    "num_class": num_class,
                },
                num_boost_round=params["num_boost_round"],
                train_set=train_data,
                valid_sets=[train_data, val_data],
                valid_names=["train", "val"],
                callbacks=[
                    lgb.early_stopping(stopping_rounds=params["early_stopping_rounds"]),
                    lgb.record_evaluation(evals_result),
                    tensorboard_callback,
                ],
            )
        else:

            class TensorBoardCallback(xgb.callback.TrainingCallback):

                def __init__(self, log_dir: str):
                    self.writer = SummaryWriter(log_dir=log_dir)

                def after_iteration(
                    self,
                    model,
                    epoch: int,
                    evals_log: xgb.callback.TrainingCallback.EvalsLog,
                ) -> bool:
                    if not evals_log:
                        return False

                    for data, metric in evals_log.items():
                        for metric_name, log in metric.items():
                            score = (
                                log[-1][0] if isinstance(log[-1], tuple) else log[-1]
                            )
                            self.writer.add_scalar(f"XGBoost/{data}", score, epoch)

                    return False

            tensorboard_callback = TensorBoardCallback(self.log_dir)

            loss = (
                "reg:squarederror"
                if self.target_type == "regression"
                else ("binary:logistic" if num_class <= 2 else "multi:softprob")
            )
            eval_metric = (
                "rmse"
                if self.target_type == "regression"
                else ("logloss" if num_class <= 2 else "mlogloss")
            )
            model = xgb.train(
                params={
                    **params["model_params"],
                    "objective": loss,
                    "eval_metric": eval_metric,
                    "num_class": num_class,
                },
                num_boost_round=params["num_boost_round"],
                dtrain=train_data,
                evals=[(val_data, "val"), (train_data, "train")],
                callbacks=[
                    xgb.callback.EarlyStopping(
                        rounds=params["early_stopping_rounds"], save_best=True
                    ),
                    xgb.callback.EvaluationMonitor(),  # This shows evaluation results at each iteration
                    tensorboard_callback,
                ],
                evals_result=evals_result,  # Record evaluation result
                verbose_eval=0,
            )

        model.model_name = self.create_model
        model.target_type = self.target_type
        logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")

        # Close the writer after training is done
        writer.close()

        if self.plot:
            # Plot loss per epoch
            train_loss = evals_result["train"][eval_metric]
            val_loss = evals_result["val"][eval_metric]
            logs = pd.DataFrame({"train": train_loss, "val": val_loss})

            plt.figure(figsize=(14, 4))
            plt.plot(logs.loc[:, "train"], lw=2, label="Training loss")
            plt.plot(logs.loc[:, "val"], lw=2, label="Validation loss")
            plt.xlabel("Epoch")
            plt.ylabel("Loss")
            plt.legend()
            plt.show()

        self._model = model

        return model

    def fit_recurrent(self, x_train, y_train, x_val, y_val, params):

        # metrics functions
        def rmse_tf(y_true, y_pred):
            y_true, y_pred = unscale_tf(y_true, y_pred)
            results = K.sqrt(K.mean(K.square(y_pred - y_true)))
            return results

        def mae_tf(y_true, y_pred):
            y_true, y_pred = unscale_tf(y_true, y_pred)
            results = K.mean(K.abs(y_pred - y_true))
            return results

        def unscale_tf(y_true, y_pred):
            if self.target_type == "regression":
                scale = K.constant(self.scaler_y.scale_[0])
                mean = K.constant(self.scaler_y.mean_[0])

                y_true = K.mul(y_true, scale)
                y_true = K.bias_add(y_true, mean)

                y_pred = K.mul(y_pred, scale)
                y_pred = K.bias_add(y_pred, mean)
            return y_true, y_pred

        # Create the model
        labels = np.unique(y_train[:, 0])
        num_class = labels.size if self.target_type == "classification" else None
        input_shape = (x_train.shape[1], x_train.shape[2])
        model = self.create_model(params, input_shape, self.target_type, num_class)
        model.target_type = self.target_type

        # Compile the model
        loss = (
            rmse_tf
            if self.target_type == "regression"
            else (
                BinaryCrossentropy(from_logits=False)
                if num_class <= 2
                else CategoricalCrossentropy(from_logits=False)
            )
        )
        optimizer = Adam(
            learning_rate=params["learning_rate"], clipnorm=params["clipnorm"]
        )
        metrics = (
            [mae_tf]
            if self.target_type == "regression"
            else (
                ["accuracy", Precision(), Recall()]
                if num_class <= 2
                else ["categorical_accuracy"]
            )
        )
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        # Callbacks
        tensorboard_callback = TensorBoard(log_dir=self.log_dir)
        early_stopping_callback = EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
            start_from_epoch=5,
        )

        # Custom callbacks
        class PrintTrainableWeights(keras.callbacks.Callback):
            def on_epoch_end(self, epoch, logs={}):
                logger.info(model.trainable_variables)

        class GradientCalcCallback(keras.callbacks.Callback):
            def __init__(self):
                self.epoch_gradient = []

            def get_gradient_func(self, model):
                # grads = K.gradients(model.total_loss, model.trainable_weights)
                grads = K.gradients(model.loss, model.trainable_weights)
                # inputs = model.model.inputs + model.targets + model.sample_weights
                # use below line of code if above line doesn't work for you
                # inputs = model.model._feed_inputs + model.model._feed_targets + model.model._feed_sample_weights
                inputs = (
                    model._feed_inputs
                    + model._feed_targets
                    + model._feed_sample_weights
                )
                func = K.function(inputs, grads)
                return func

            def on_epoch_end(self, epoch, logs=None):
                get_gradient = self.get_gradient_func(model)
                grads = get_gradient([x_val, y_val[:, 0], np.ones(len(y_val[:, 0]))])
                self.epoch_gradient.append(grads)

        # Train the model
        if self.target_type == "classification" and num_class > 2:
            lb = LabelBinarizer(sparse_output=False)  # Change to True for sparse matrix
            lb.fit(labels)
            y_train = lb.transform(y_train[:, 0].flatten())
            y_val = lb.transform(y_val[:, 0].flatten())
        else:
            y_train = y_train[:, 0].flatten()
            y_val = y_val[:, 0].flatten()

        logger.info("Fitting the model...")
        logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
        logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

        history = model.fit(
            x_train,
            y_train,
            batch_size=params["batch_size"],
            verbose=0,
            epochs=params["epochs"],
            shuffle=False,
            validation_data=(x_val, y_val),
            callbacks=[early_stopping_callback, tensorboard_callback],
        )

        logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")
        # logger.info(pd.DataFrame(gradiant.epoch_gradient))

        if self.plot:
            # Plot loss per epoch
            logs = pd.DataFrame(history.history)

            plt.figure(figsize=(14, 4))
            plt.plot(logs.loc[:, "loss"], lw=2, label="Training loss")
            plt.plot(logs.loc[:, "val_loss"], lw=2, label="Validation loss")
            plt.xlabel("Epoch")
            plt.ylabel("Loss")
            plt.legend()
            plt.show()

        self._model = model

        return model

    def predict(
        self,
        data: pd.DataFrame,
        threshold: float = 0.5,
    ):
        """Function to get prediction from model. Support sklearn, keras and boosting models such as xgboost and lgboost

        Args:
            - data: the data for prediction
            - threshold: the threshold for classification
        """
        if not self._model:
            raise Exception(
                "Model is not fitted, cannot predict, run model.fit() first, or pass a fitted model when creating the Model object to the `model` parameter."
            )
        model = self._model

        if self.threshold and threshold == 0.5:
            threshold = self.threshold

        if self.recurrent or model.model_name in ["lgb", "xgb"]:
            # keras, lgb & xgb
            if model.model_name == "lgb":
                # Direct prediction for LightGBM
                pred = model.predict(data)
            elif model.model_name == "xgb":
                # Convert val_data to DMatrix for XGBoost
                d_data = xgb.DMatrix(data)
                pred = model.predict(d_data)
            else:
                # Reshape (flatten) for keras if not multiclass
                pred = model.predict(data)
                if pred.shape[1] == 1:
                    pred = pred.reshape(-1)

            if self.target_type == "classification":
                num_class = pred.shape[1] if len(pred.shape) > 1 else 2

                if num_class <= 2:
                    # For binary classification, concatenate the predicted probabilities for both classes
                    pred_df = pd.DataFrame(
                        {
                            0: 1 - pred,  # Probability of class 0
                            1: pred,  # Probability of class 1
                        },
                    )
                else:
                    # For multi-class classification, use the predicted probabilities for each class
                    pred_df = pd.DataFrame(pred, columns=range(num_class))

                # Get final predictions (argmax for multi-class, threshold for binary)
                if num_class == 2:
                    pred_df["PRED"] = np.where(
                        pred_df[1] >= threshold, 1, 0
                    )  # Class 1 if prob >= threshold
                else:
                    pred_df["PRED"] = pred_df.idxmax(
                        axis=1
                    )  # Class with highest probability for multiclasses

                # Reorder columns to show predicted class first, then probabilities
                pred = pred_df[["PRED"] + list(range(num_class))]

            else:
                pred = pd.Series(pred, name="PRED")

            # set index for lgb and xgb (for keras, as we use np array, we need to set index outside)
            if model.model_name in ["lgb", "xgb"]:
                pred.index = data.index
        else:
            # sk learn
            pred = pd.Series(model.predict(data), index=data.index, name="PRED")
            if self.target_type == "classification":
                pred_proba = pd.DataFrame(
                    model.predict_proba(data),
                    index=data.index,
                    columns=[
                        int(c) if isinstance(c, float) and c.is_integer() else c
                        for c in model.classes_
                    ],
                )

                # Apply threshold for binary classification
                if len(model.classes_) == 2:
                    positive_class = model.classes_[1]  # Assuming classes are ordered
                    pred = (pred_proba[positive_class] >= threshold).astype(int)
                    pred.name = "PRED"

                pred = pd.concat([pred, pred_proba], axis=1)

        return pred

    def save(self, path):
        if self.recurrent:
            path += "/" + self.model_name + ".keras"
            self._model.save(path)
        else:
            path += "/" + self.model_name + ".best"
            joblib.dump(self._model, path)
        self.path = path
        return path

    def load(self):
        if not self.path:
            raise ValueError("Path is not set, cannot load model")

        training_target_dir = Path(self.path)

        # Load threshold
        scores_tracking = pd.read_csv(f"{training_target_dir}/scores_tracking.csv")
        self.threshold = (
            scores_tracking["THRESHOLD"].values[0]
            if "THRESHOLD" in scores_tracking.columns
            else None
        )

        # Search for files that contain '.best' or '.keras' in the name
        best_files = list(training_target_dir.glob("*.best*")) + list(
            training_target_dir.glob("*.keras*")
        )
        # If any files are found, try loading the first one (or process as needed)
        if best_files:
            file_path = best_files[
                0
            ]  # Assuming you want to open the first matching file
            try:
                # Attempt to load the file as a scikit-learn, XGBoost, or LightGBM model (Pickle format)
                self._model = joblib.load(file_path)
                logger.info(
                    f"Loaded model {self._model.model_name} and threshold {self.threshold}"
                )
            except (pickle.UnpicklingError, EOFError):
                # If it's not a pickle file, try loading it as a Keras model
                try:
                    # Attempt to load the file as a Keras model
                    self._model = keras.models.load_model(file_path)
                    logger.info(
                        f"Loaded model {self._model.model_name} and threshold {self.threshold}"
                    )
                except Exception as e:
                    raise FileNotFoundError(
                        f"Model could not be loaded from path: {file_path}: {e}"
                    )
        else:
            raise FileNotFoundError(
                f"No files with '.best' or '.keras' found in the specified folder: {training_target_dir}"
            )

        self.model_name = self._model.model_name
        self.target_type = self._model.target_type

    def __getattr__(self, attr):
        return getattr(self._model, attr)


def trainable(
    params,
    x_train,
    y_train,
    x_val,
    y_val,
    model_name,
    target_type,
    session_name,
    target_number,
    create_model,
    type_name="hyperopts",
    plot=False,
):
    """Standalone version of train_model that doesn't depend on self"""
    # Create model engine
    model = ModelEngine(
        model_name=model_name,
        target_type=target_type,
        create_model=create_model,
        plot=plot,
    )

    logger.info(
        f"TARGET_{target_number} - Training a {model.model_name} at {datetime.now()} : {session_name}, TARGET_{target_number}"
    )

    if model.recurrent:
        timesteps = params["timesteps"]
        x_train = x_train[:, -timesteps:, :]
        x_val = x_val[:, -timesteps:, :]

    # Compile and fit model on train set
    start = time.time()
    model.fit(x_train, y_train, x_val, y_val, params)
    stop = time.time()

    # Prediction on val set
    y_pred = model.predict(x_val)

    # fix for recurrent model because x_val has no index as it is a 3D np array
    if model.recurrent:
        y_val = pd.DataFrame(y_val, columns=["TARGET", "index"]).set_index("index")
        y_pred.index = y_val.index

    prediction = pd.concat([y_val, y_pred], axis=1)

    # Unscale the data
    if (
        model.need_scaling
        and model.target_type == "regression"
        and model.scaler_y is not None
    ):
        # scaler_y needs 2D array with shape (-1, 1)
        prediction.loc[:, "TARGET"] = model.scaler_y.inverse_transform(
            prediction[["TARGET"]].values
        )
        prediction.loc[:, "PRED"] = model.scaler_y.inverse_transform(
            prediction[["PRED"]].values
        )

    # Evaluate model
    score = {
        "DATE": datetime.now(),
        "SESSION": session_name,
        "TRAIN_DATA": x_train.shape[0],
        "VAL_DATA": x_val.shape[0],
        "FEATURES": x_train.shape[-1],
        "MODEL_NAME": model.model_name,
        "TYPE": type_name,
        "TRAINING_TIME": stop - start,
        "EVAL_DATA_STD": prediction["TARGET"].std(),
    }

    score.update(evaluate(prediction, target_type))

    if type_name == "hyperopts":
        session.report(metrics=score)
        return score

    return score, model, prediction


class ModelSelectionEngine:

    def __init__(
        self,
        data,
        reshaped_data,
        target_number,
        target_clf,
        dataset,
        models_idx,
        time_series,
        date_column,
        group_column,
        **kwargs,
    ):
        self.data = data
        self.reshaped_data = reshaped_data
        self.target_number = target_number
        self.dataset = dataset
        self.target_clf = target_clf
        self.models_idx = models_idx
        self.time_series = time_series
        self.date_column = date_column
        self.group_column = group_column

        self.target_type = (
            "classification" if self.target_number in self.target_clf else "regression"
        )
        self.dataset_dir = self.dataset.path
        self.dataset_id = self.dataset.id
        self.data_dir = f"{self.dataset_dir}/data"
        self.preprocessing_dir = f"{self.dataset_dir}/preprocessing"
        self.training_target_dir = f"{self.dataset_dir}/TARGET_{self.target_number}"
        self.metric = "RMSE" if self.target_type == "regression" else "LOGLOSS"
        self.features = self.dataset.get_features(self.target_number)
        self.all_features = self.dataset.get_all_features(
            date_column=self.date_column, group_column=self.group_column
        )

    # Main training function
    def run(
        self,
        session_name,
        perform_hyperopt=True,
        number_of_trials=20,
        perform_crossval=False,
        plot=True,
        clean_dir=False,  # TODO: This has been unused because now feature_selection is in the target directory
        preserve_model=True,
    ):
        """
        Selects the best models based on a target variable, optionally performing hyperparameter optimization
        and cross-validation, and manages outputs in a session-specific directory.
        """
        self.session_name = session_name
        self.plot = plot
        self.number_of_trials = number_of_trials

        if self.dataset_id is None:
            raise ValueError("Please provide a dataset.")

        if self.data:
            self.train = self.data["train"]
            self.val = self.data["val"]
            self.test = self.data["test"]
            self.train_scaled = self.data["train_scaled"]
            self.val_scaled = self.data["val_scaled"]
            self.test_scaled = self.data["test_scaled"]
        else:
            (
                self.train,
                self.val,
                self.test,
                self.train_scaled,
                self.val_scaled,
                self.test_scaled,
            ) = load_train_data(self.dataset_dir, self.target_number, self.target_clf)

        if (
            any(all_models[i].get("recurrent") for i in self.models_idx)
            and not self.time_series
        ):
            ValueError(
                "You need to set time_series to true to use recurrent model, or remove recurrent models from models_idx chosen"
            )

        if (
            any(all_models[i].get("recurrent") for i in self.models_idx)
            and self.time_series
        ):
            if self.reshaped_data is None:
                raise ValueError("reshaped_data is not provided.")

            logger.info("Loading reshaped data...")
            self.x_train_reshaped = self.reshaped_data["x_train_reshaped"]
            self.y_train_reshaped = self.reshaped_data["y_train_reshaped"]
            self.x_val_reshaped = self.reshaped_data["x_val_reshaped"]
            self.y_val_reshaped = self.reshaped_data["y_val_reshaped"]

        # create model selection in db
        target = Target.find_by(name=f"TARGET_{self.target_number}")
        model_selection = ModelSelection.upsert(
            match_fields=["target_id", "dataset_id"],
            target_id=target.id,
            dataset_id=self.dataset_id,
        )

        # recurrent models starts at 9 # len(list_models)
        for i in self.models_idx:
            config = all_models[i]
            recurrent = config["recurrent"]
            need_scaling = config["need_scaling"]
            model_name = config["model_name"]

            if recurrent is False and config[self.target_type] is None:
                continue  # for naive bayes models that cannot be used in regression

            self.results_dir = f"{self.training_target_dir}/{model_name}"
            if not os.path.exists(f"{self.results_dir}"):
                os.makedirs(f"{self.results_dir}")
            elif preserve_model and contains_best(self.results_dir):
                continue
            elif perform_hyperopt:
                clean_directory(self.results_dir)

            logger.info(f"Training a {model_name}")
            model = Model.upsert(
                match_fields=["name", "type"],
                name=model_name,
                type=self.target_type,
            )
            model_training = ModelTraining.upsert(
                match_fields=["model_id", "model_selection_id"],
                model_id=model.id,
                model_selection_id=model_selection.id,
            )

            # getting data
            if recurrent:
                # Clear cluster from previous Keras session graphs.
                K.clear_session()

                features_idx = [
                    i
                    for i, e in enumerate(self.all_features)
                    if e in set(self.features)
                ]
                # TODO: Verify that features_idx are the right one, because scaling can re-arrange columns...
                self.x_train = self.x_train_reshaped[:, :, features_idx]
                self.y_train = self.y_train_reshaped[:, [self.target_number, 0]]
                self.x_val = self.x_val_reshaped[:, :, features_idx]
                self.y_val = self.y_val_reshaped[:, [self.target_number, 0]]
            else:
                config = config[self.target_type]

                if need_scaling and self.target_type == "regression":
                    self.x_train = self.train_scaled[self.features]
                    self.y_train = self.train_scaled[
                        f"TARGET_{self.target_number}"
                    ].rename("TARGET")
                    self.x_val = self.val_scaled[self.features]
                    self.y_val = self.val_scaled[f"TARGET_{self.target_number}"].rename(
                        "TARGET"
                    )
                else:
                    self.x_train = self.train[self.features]
                    self.y_train = self.train[f"TARGET_{self.target_number}"].rename(
                        "TARGET"
                    )
                    self.x_val = self.val[self.features]
                    self.y_val = self.val[f"TARGET_{self.target_number}"].rename(
                        "TARGET"
                    )

            log_dir = get_log_dir(self.training_target_dir, model_name)
            # instantiate model
            model = ModelEngine(
                model_name=model_name,
                search_params=config["search_params"],
                target_type=self.target_type,
                create_model=config["create_model"],
                plot=self.plot,
                log_dir=log_dir,
            )

            start = time.time()
            # Tuning hyperparameters
            if perform_hyperopt:
                best_params = self.hyperoptimize(model)

                # save best params
                best_params_file = f"{self.training_target_dir}/best_params.json"
                try:
                    with open(best_params_file, "r") as f:
                        json_dict = json.load(f)
                except FileNotFoundError:
                    json_dict = {}

                json_dict[model.model_name] = serialize_for_json(best_params)
                with open(best_params_file, "w") as f:
                    json.dump(json_dict, f, indent=4)
            else:
                try:
                    with open(f"{self.training_target_dir}/best_params.json") as f:
                        json_dict = json.load(f)
                        best_params = json_dict[model_name]
                except Exception:
                    raise FileNotFoundError(
                        f"Could not find {model_name} in current data. Try to run an hyperoptimization by setting `perform_hyperopt` to true"
                    )

            # Perform cross-validation of the best model on k-folds of train + val set
            if perform_crossval:
                x_train_val = pd.concat([self.x_train, self.x_val, self.x_test], axis=0)
                y_train_val = pd.concat([self.y_train, self.y_val, self.y_test], axis=0)
                n_splits = 4
                n_samples = len(x_train_val)
                test_size = int(n_samples / (n_splits + 4))
                tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

                # Store the scores
                cross_validation_scores = []

                for i, (train_index, val_index) in enumerate(tscv.split(x_train_val)):
                    self.type_name = f"crossval_fold_{i}"

                    if self.time_series:
                        date_series = self.train[self.date_column].copy()

                        if need_scaling:
                            date_series = date_series.map(pd.Timestamp.fromordinal)

                        # Now you can use the actual train/val indices to extract ranges
                        train_start = date_series.iloc[train_index[0]]
                        train_end = date_series.iloc[train_index[-1]]
                        val_start = date_series.iloc[val_index[0]]
                        val_end = date_series.iloc[val_index[-1]]

                        logger.info(
                            f"[Fold {i}] Train: {len(train_index)} samples from {train_start.date()} to {train_end.date()} | "
                            f"Validation: {len(val_index)} samples from {val_start.date()} to {val_end.date()}"
                        )
                    else:
                        logger.info(
                            f"[Fold {i}] Train: {len(train_index)} samples | Validation: {len(val_index)} samples"
                        )

                    # Train the model and get the score
                    if recurrent:
                        cross_validation_score, _, _ = self.train_model(
                            params=best_params,
                            x_train=x_train_val[train_index],
                            y_train=y_train_val[train_index],
                            x_val=x_train_val[val_index],
                            y_val=y_train_val[val_index],
                            model=model,
                        )
                    else:
                        cross_validation_score, _, _ = self.train_model(
                            params=best_params,
                            x_train=x_train_val.iloc[train_index],
                            y_train=y_train_val.iloc[train_index],
                            x_val=x_train_val.iloc[val_index],
                            y_val=y_train_val.iloc[val_index],
                            model=model,
                        )

                    # Append score to the list
                    cross_validation_scores.append(cross_validation_score)

                # Calculate and log the mean score
                cross_validation_mean_score = pd.DataFrame(cross_validation_scores)[
                    self.metric
                ].mean()
                logger.info(
                    f"Best model mean cross-validation score on entire dataset: {cross_validation_mean_score}"
                )

                # Retrain on entire training set, but keep score on cross-validation folds
                best_score, best_model, best_pred = self.train_model(
                    params=best_params,
                    x_train=pd.concat([self.x_train, self.x_val], axis=0),
                    y_train=pd.concat([self.y_train, self.y_val], axis=0),
                    x_val=self.x_test,
                    y_val=self.y_test,
                    model=model,
                )
                best_score = cross_validation_mean_score
            else:
                # Evaluate on validation set
                self.type_name = "validation"
                best_score, best_model, best_pred = self.train_model(
                    params=best_params,
                    x_train=pd.concat([self.x_train, self.x_val], axis=0),
                    y_train=pd.concat([self.y_train, self.y_val], axis=0),
                    x_val=self.x_test,
                    y_val=self.y_test,
                    model=model,
                )

                logger.info(f"Best model scores on test set: {best_score}")

            # Save validation predictions
            best_pred.to_csv(
                f"{self.results_dir}/pred_val.csv",
                index=True,
                header=True,
                index_label="ID",
            )

            # Save best model
            model_path = best_model.save(self.results_dir)

            model_path = Path(model_path).resolve()
            best_score["MODEL_PATH"] = model_path

            # Track scores
            scores_tracking_path = f"{self.training_target_dir}/scores_tracking.csv"
            best_score_df = pd.DataFrame([best_score])

            if os.path.exists(scores_tracking_path):
                existing_scores = pd.read_csv(scores_tracking_path)
                common_cols = existing_scores.columns.intersection(
                    best_score_df.columns
                )
                best_score_df = best_score_df[common_cols]
                scores_tracking = pd.concat(
                    [existing_scores, best_score_df], ignore_index=True
                )
            else:
                scores_tracking = best_score_df

            scores_tracking.sort_values(self.metric, ascending=True, inplace=True)
            scores_tracking.to_csv(scores_tracking_path, index=False)

            # Save model training metadata
            stop = time.time()
            training_time = stop - start
            model_training.best_params = best_params
            model_training.model_path = model_path
            model_training.training_time = training_time
            model_training.save()

            # Store metrics in DB
            drop_cols = [
                "DATE",
                "SESSION",
                "TRAIN_DATA",
                "VAL_DATA",
                "FEATURES",
                "MODEL_NAME",
                "MODEL_PATH",
            ]
            best_score = {k: v for k, v in best_score.items() if k not in drop_cols}
            score_data = {k.lower(): v for k, v in best_score.items()}

            Score.upsert(
                match_fields=["model_training_id"],
                model_training_id=model_training.id,
                **score_data,
            )

            logger.info(f"Model training finished in {training_time:.2f} seconds")

        # find best model type
        scores_tracking_path = f"{self.training_target_dir}/scores_tracking.csv"
        scores_tracking = pd.read_csv(scores_tracking_path)
        best_score_overall = scores_tracking.iloc[0, :]
        best_model_name = best_score_overall["MODEL_NAME"]

        # Remove any .best or .keras files
        for file_path in glob.glob(
            os.path.join(self.training_target_dir, "*.best")
        ) + glob.glob(os.path.join(self.training_target_dir, "*.keras")):
            os.remove(file_path)
        # Copy the best model in root training folder for this target
        best_model_path = Path(
            f"{self.training_target_dir}/{os.path.basename(best_score_overall['MODEL_PATH'])}"
        ).resolve()
        copy_any(
            best_score_overall["MODEL_PATH"],
            best_model_path,
        )

        with open(f"{self.training_target_dir}/best_params.json", "r") as f:
            best_model_params = json.load(f)[best_model_name]

        # save model_selection results to db
        model_selection = ModelSelection.get(model_selection.id)
        model_selection.best_model_id = Model.find_by(
            name=best_score_overall["MODEL_NAME"], type=self.target_type
        ).id
        model_selection.best_model_params = best_model_params
        model_selection.best_model_path = best_model_path
        model_selection.save()

        logger.info(f"Best model overall is : {best_score_overall}")

    def hyperoptimize(self, model: ModelEngine):
        self.type_name = "hyperopts"

        def collect_error_logs(training_target_dir: int, storage_path: str):
            output_error_file = f"{training_target_dir}/errors.log"

            with open(output_error_file, "a") as outfile:
                # Walk through the ray_results directory
                for root, dirs, files in os.walk(storage_path):
                    # Check if 'error.txt' exists in the current directory
                    if "error.txt" in files:
                        error_file_path = os.path.join(root, "error.txt")
                        logger.info(f"Processing error file: {error_file_path}")
                        # Read and append the content of the error.txt file
                        with open(error_file_path, "r") as infile:
                            outfile.write(f"\n\n=== Error from {error_file_path} ===\n")
                            outfile.write(infile.read())
            logger.info(f"All errors written to {output_error_file}")

        logger.info("Start tuning hyperparameters...")

        storage_path = f"{self.results_dir}/ray_results"

        tuner = Tuner(
            trainable=with_parameters(
                trainable,
                x_train=self.x_train,
                y_train=self.y_train,
                x_val=self.x_val,
                y_val=self.y_val,
                model_name=model.model_name,
                target_type=self.target_type,
                session_name=self.session_name,
                target_number=self.target_number,
                create_model=model.create_model,
                type_name="hyperopts",
                plot=model.plot,
            ),
            param_space=model.search_params,
            tune_config=TuneConfig(
                metric=self.metric,
                mode="min",
                search_alg=HyperOptSearch(),
                num_samples=self.number_of_trials,
                scheduler=ASHAScheduler(max_t=100, grace_period=10),
            ),
            run_config=RunConfig(
                stop={"training_iteration": 100},
                storage_path=storage_path,
                callbacks=[TBXLoggerCallback()],
            ),
        )
        try:
            results = tuner.fit()

            best_result = results.get_best_result(self.metric, "max")
            best_params = best_result.config
            best_score = best_result.metrics

            # log results
            logger.info(f"Best hyperparameters found were:\n{best_params}")
            logger.info(f"Best Scores found were:\n{best_score}")
            logger.info(
                f"Markdown table with all trials :\n{results.get_dataframe().to_markdown()}"
            )
            # Collect errors in single file
            collect_error_logs(
                training_target_dir=self.training_target_dir, storage_path=storage_path
            )

        except Exception as e:
            raise Exception(e)

        finally:
            ray.shutdown()

        return best_params

    def train_model(self, params, x_train, y_train, x_val, y_val, model: ModelEngine):
        # Use the standalone training function to avoid duplication
        # For train_model, we pass the data directly (not as Ray references)
        return trainable(
            params,
            x_train,
            y_train,
            x_val,
            y_val,
            model.model_name,
            self.target_type,
            self.session_name,
            self.target_number,
            model.create_model,
            self.type_name,
            model.plot,
        )


def evaluate(prediction: pd.DataFrame, target_type: str):
    """
    Function to evaluate model performance

    Args:
        - prediction: the prediction dataframe containing TARGET and PRED columns, as well as predicted probablities for each class for classification tasks
        - target_type: classification or regression
    """
    score = {}
    y_true = prediction["TARGET"]
    y_pred = prediction["PRED"]

    if target_type == "regression":
        # Main metrics
        score["RMSE"] = root_mean_squared_error(y_true, y_pred)
        score["MAE"] = mean_absolute_error(y_true, y_pred)
        score["MAPE"] = mean_absolute_percentage_error(y_true, y_pred)
        score["R2"] = r2_score(y_true, y_pred)

        # Robustness: avoid division by zero
        std_target = y_true.std()
        mean_target = y_true.mean()
        median_target = y_true.median()

        # RMSE / STD
        score["RMSE_STD_RATIO"] = (
            float(100 * score["RMSE"] / std_target) if std_target else 1000
        )

        # Median absolute deviation (MAD)
        mam = (y_true - mean_target).abs().median()  # Median Abs around Mean
        mad = (y_true - median_target).abs().median()  # Median Abs around Median
        score["MAM"] = mam
        score["MAD"] = mad
        score["MAE_MAM_RATIO"] = (
            float(100 * score["MAE"] / mam) if mam else 1000
        )  # MAE / MAD → Plus stable, moins sensible aux outliers.
        score["MAE_MAD_RATIO"] = (
            float(100 * score["MAE"] / mad) if mad else 1000
        )  # MAE / Médiane des écarts absolus autour de la moyenne: Moins robuste aux outliers

    else:

        labels = np.unique(y_true)
        num_classes = labels.size
        y_pred_proba = (
            prediction[1] if num_classes == 2 else prediction.iloc[:, 2:].values
        )
        if num_classes > 2:
            lb = LabelBinarizer(sparse_output=False)  # Change to True for sparse matrix
            lb.fit(labels)
            y_true_onhot = lb.transform(y_true)
            y_pred_onehot = lb.transform(y_pred)

        score["LOGLOSS"] = log_loss(y_true, y_pred_proba)
        score["ACCURACY"] = accuracy_score(y_true, y_pred)
        score["PRECISION"] = precision_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["RECALL"] = recall_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["F1"] = f1_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["ROC_AUC"] = float(roc_auc_score(y_true, y_pred_proba, multi_class="ovr"))
        (
            score["THRESHOLD"],
            score["PRECISION_AT_THRESHOLD"],
            score["RECALL_AT_THRESHOLD"],
        ) = (
            find_best_precision_threshold(prediction)
            if num_classes == 2
            else (None, None, None)
        )
    return score


# utils
def get_log_dir(training_target_dir: str, model_name="test_model"):
    """Generates a structured log directory path for TensorBoard."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_dir = (
        Path(training_target_dir + "/tensorboard") / model_name / f"run_{timestamp}"
    )
    log_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
    return str(log_dir)


def print_scores(training_target_dir: str):
    """
    Monitor scores
    """
    scores_tracking = pd.read_csv(f"{training_target_dir}/scores_tracking.csv")
    return scores_tracking


# plots
def plot_evaluation_for_classification(prediction: dict):
    """
    Args
        prediction (pd.DataFrame): Should be a df with TARGET, PRED, 0, 1 columns for y_true value (TARGET), y_pred (PRED), and probabilities (for classification only : 0 and 1)
    """
    y_true = prediction["TARGET"]
    y_pred = prediction["PRED"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Plot confusion matrix
    plot_confusion_matrix(y_true, y_pred)

    # Compute ROC curve and ROC area
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 8))
    plt.plot(
        fpr, tpr, color="darkorange", lw=2, label="ROC curve (area = %0.2f)" % roc_auc
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.show()

    # Compute precision-recall curve
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    average_precision = average_precision_score(y_true, y_pred_proba)

    plt.figure(figsize=(8, 8))
    plt.step(recall, precision, color="b", alpha=0.2, where="post")
    plt.fill_between(recall, precision, step="post", alpha=0.2, color="b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title("Precision-Recall Curve: AP={0:0.2f}".format(average_precision))
    plt.show()


def plot_confusion_matrix(y_true, y_pred):
    unique_labels = np.unique(np.concatenate((y_true, y_pred)))
    cm = confusion_matrix(y_true, y_pred)

    labels = np.sort(unique_labels)  # Sort labels based on numerical order

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="viridis")
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("True", fontsize=12)
    plt.title("Confusion Matrix", fontsize=14)

    plt.xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=10)
    plt.yticks(ticks=np.arange(len(labels)), labels=labels, fontsize=10)

    plt.show()


# thresholds
def find_max_f1_threshold(prediction):
    """
    Finds the threshold that maximizes the F1 score for a binary classification task.

    Parameters:
    - prediction: DataFrame with 'TARGET' and '1' (predicted probabilities) columns

    Returns:
    - best_threshold: The threshold that maximizes the F1 score
    - best_precision: The precision at that threshold
    - best_recall: The recall at that threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Compute precision, recall, and thresholds
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Drop the first element to align with thresholds
    precision = precision[1:]
    recall = recall[1:]

    # Filter out trivial cases (precision or recall = 0)
    valid = (precision > 0) & (recall > 0)
    if not np.any(valid):
        raise ValueError("No valid threshold with non-zero precision and recall")

    precision = precision[valid]
    recall = recall[valid]
    thresholds = thresholds[valid]

    # Compute F1 scores for each threshold
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)

    best_index = np.argmax(f1_scores)

    best_threshold = thresholds[best_index]
    best_precision = precision[best_index]
    best_recall = recall[best_index]

    return best_threshold, best_precision, best_recall


def find_best_f1_threshold(prediction, fscore_target: float):
    """
    Finds the highest threshold achieving at least the given F1 score target.

    Parameters:
    - prediction: DataFrame with 'TARGET' and '1' (or 1 as int) columns
    - fscore_target: Desired minimum F1 score (between 0 and 1)

    Returns:
    - best_threshold: The highest threshold meeting the F1 target
    - best_precision: Precision at that threshold
    - best_recall: Recall at that threshold
    - best_f1: Actual F1 score at that threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Align precision/recall with thresholds
    precision = precision[1:]
    recall = recall[1:]
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)

    # Filter for thresholds meeting F1 target
    valid_indices = [i for i, f1 in enumerate(f1_scores) if f1 >= fscore_target]

    if not valid_indices:
        raise ValueError(f"Could not find a threshold with F1 >= {fscore_target:.2f}")

    # Pick the highest threshold among valid ones
    best_index = valid_indices[-1]

    return (
        thresholds[best_index],
        precision[best_index],
        recall[best_index],
        f1_scores[best_index],
    )


def find_max_precision_threshold_without_trivial_case(prediction: dict):
    """
    Finds the threshold that maximizes precision without reaching a precision of 1,
    which indicates all predictions are classified as the negative class (0).

    Parameters:
    - prediction: dict with keys 'TARGET' (true labels) and '1' (predicted probabilities)

    Returns:
    - threshold: the probability threshold that maximizes precision
    - actual_recall: the recall achieved at this threshold
    - actual_precision: the precision achieved at this threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Compute precision, recall, and thresholds
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Drop the first element of precision and recall to align with thresholds
    precision = precision[1:]
    recall = recall[1:]

    # Filter out precision == 1.0 (which might correspond to predicting only 0s)
    valid_indices = np.where(precision < 1.0)[0]
    if len(valid_indices) == 0:
        raise ValueError("No valid precision values less than 1.0")

    precision = precision[valid_indices]
    recall = recall[valid_indices]
    thresholds = thresholds[valid_indices]

    # Find the index of the maximum precision
    best_index = np.argmax(precision)

    # Return the corresponding threshold, precision, and recall
    best_threshold = thresholds[best_index]
    best_precision = precision[best_index]
    best_recall = recall[best_index]

    return best_threshold, best_precision, best_recall


def find_best_precision_threshold(prediction, precision_target: float = 0.80):
    """
    Finds the highest threshold that achieves at least the given precision target.

    Parameters:
        prediction (pd.DataFrame): DataFrame with columns 'TARGET' and '1' or index 1 for predicted probabilities
        precision_target (float): Desired minimum precision (between 0 and 1)

    Returns:
        tuple: (threshold, precision, recall) achieving the desired precision
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Align lengths: thresholds is N-1 compared to precision/recall
    thresholds = thresholds
    precision = precision[1:]  # Shift to match thresholds
    recall = recall[1:]

    valid_indices = [i for i, p in enumerate(precision) if p >= precision_target]

    if not valid_indices:
        raise ValueError(
            f"Could not find a threshold with precision >= {precision_target}"
        )

    best_idx = valid_indices[-1]  # Highest threshold with precision >= target

    return thresholds[best_idx], precision[best_idx], recall[best_idx]


def find_best_recall_threshold(prediction, recall_target: float = 0.98) -> float:
    """
    Finds the highest threshold that achieves at least the given recall target.

    Parameters:
        pred_df (pd.DataFrame): DataFrame with columns 'y_true' and 'y_pred_proba'
        recall_target (float): Desired minimum recall (between 0 and 1)

    Returns:
        float: Best threshold achieving the desired recall, or None if not reachable
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # `thresholds` has length N-1 compared to precision and recall
    recall = recall[1:]  # Drop first element to align with thresholds
    precision = precision[1:]

    valid_indices = [i for i, r in enumerate(recall) if r >= recall_target]

    if not valid_indices:
        logger.warning(f"Could not find a threshold with recall >= {recall_target}")
        return None, None, None

    best_idx = valid_indices[-1]  # Highest threshold with recall >= target

    return thresholds[best_idx], precision[best_idx], recall[best_idx]


def plot_threshold(prediction, threshold, precision, recall):
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]
    y_true = prediction["TARGET"]

    predicted_positive = (y_pred_proba >= threshold).sum()
    predicted_negative = (y_pred_proba < threshold).sum()
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    per_predicted_positive = predicted_positive / len(y_pred_proba)
    per_predicted_negative = predicted_negative / len(y_pred_proba)

    logger.info(
        f"""Threshold: {threshold*100:.2f}
        Precision: {precision*100:.2f}
        Recall: {recall*100:.2f}
        F1-score: {f1_scores*100:.2f}
        % of score over {threshold}: {predicted_positive}/{len(y_pred_proba)} = {per_predicted_positive*100:.2f}%
        % of score under {threshold}: {predicted_negative}/{len(y_pred_proba)} = {per_predicted_negative*100:.2f}%"""
    )

    # Visualizing the scores of positive and negative classes
    plt.figure(figsize=(10, 6))
    sns.histplot(
        y_pred_proba[y_true == 1],
        color="blue",
        label="Positive Class",
        bins=30,
        kde=True,
        alpha=0.6,
    )
    sns.histplot(
        y_pred_proba[y_true == 0],
        color="red",
        label="Negative Class",
        bins=30,
        kde=True,
        alpha=0.6,
    )
    plt.axvline(
        x=threshold,
        color="green",
        linestyle="--",
        label=f"Threshold at {round(threshold,3)}",
    )
    plt.title("Distribution of Predicted Probabilities")
    plt.xlabel("Predicted Probabilities")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
    return threshold


# OLD - to sort out
def get_pred_distribution(training_target_dir: str, model_name="linear"):
    """
    Look at prediction distributions
    """
    prediction = pd.read_csv(
        f"{training_target_dir}/{model_name}/pred_val.csv",
        index_col="ID",
    )
    prediction.describe()


def plot_feature_importance(training_target_dir: str, model_name="linear"):
    """
    Monitor feature importance ranking to filter out unrelevant features
    """
    model = joblib.load(f"{training_target_dir}/{model_name}/{model_name}.best")
    if hasattr(model, "feature_importances_"):
        feature_importances_ = model.feature_importances_.flatten()
    elif hasattr(model, "feature_importance"):
        feature_importances_ = model.feature_importance.flatten()
    elif hasattr(model, "coefs_"):
        feature_importances_ = np.mean(model.coefs_[0], axis=1).flatten()
    elif hasattr(model, "coef_"):
        feature_importances_ = model.coef_.flatten()
    else:
        feature_importances_ = []

    sns.barplot(
        data=feature_importances_,
        orient="h",
    )


def print_model_estimators(training_target_dir: str, model_name="linear"):
    """
    Look at a specific trained model
    """
    model = joblib.load(f"{training_target_dir}/{model_name}/{model_name}.best")
    for i in range(0, 100):
        logger.info(model.estimators_[i].get_depth())


def get_model_info(model):
    model.count_params()
    model.summary()
