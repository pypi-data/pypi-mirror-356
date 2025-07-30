"""
Main API class

the way I want it to work :

app = LeCrapaud()

kwargs = {

}

experiment = app.create_experiment(**kwargs) # return a class Experiment()
ou
experiment = app.get_experiment(exp_id)

best_features, artifacts, best_model = experiment.train(get_data, get_data_params)

new_data + target_pred + target_proba (if classif) = experiment.predict(**new_data)

On veut aussi pouvoir juste faire :

experiment.feature_engineering(data) : feat eng, return data

experiment.preprocess_feature(data) : split, encoding, pcas, return train, val, test df

experiment.feature_selection(train) : return features

experiment.preprocess_model(train, val, test) : return data = dict of df

experiment.model_selection(data) : return best_model
"""

import joblib
import pandas as pd
from lecrapaud.db.session import init_db
from lecrapaud.feature_selection import FeatureSelectionEngine, PreprocessModel
from lecrapaud.model_selection import ModelSelectionEngine, ModelEngine
from lecrapaud.feature_engineering import FeatureEngineeringEngine, PreprocessFeature
from lecrapaud.experiment import create_dataset
from lecrapaud.db import Dataset


class LeCrapaud:
    def __init__(self, uri: str = None):
        init_db(uri=uri)

    def create_experiment(self, **kwargs):
        return Experiment(**kwargs)

    def get_experiment(self, id: int):
        return Experiment(id)


class Experiment:
    def __init__(self, id=None, **kwargs):
        if id:
            self.dataset = Dataset.get(id)
        else:
            self.dataset = create_dataset(**kwargs)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.context = {
            # generic
            "dataset": self.dataset,
            # for FeatureEngineering
            "columns_drop": self.columns_drop,
            "columns_boolean": self.columns_boolean,
            "columns_date": self.columns_date,
            "columns_te_groupby": self.columns_te_groupby,
            "columns_te_target": self.columns_te_target,
            # for PreprocessFeature
            "time_series": self.time_series,
            "date_column": self.date_column,
            "group_column": self.group_column,
            "val_size": self.val_size,
            "test_size": self.test_size,
            "columns_pca": self.columns_pca,
            "columns_onehot": self.columns_onehot,
            "columns_binary": self.columns_binary,
            "columns_frequency": self.columns_frequency,
            "columns_ordinal": self.columns_ordinal,
            "target_numbers": self.target_numbers,
            "target_clf": self.target_clf,
            # for PreprocessModel
            "models_idx": self.models_idx,
            "max_timesteps": self.max_timesteps,
            # for ModelSelection
            "perform_hyperopt": self.perform_hyperopt,
            "number_of_trials": self.number_of_trials,
            "perform_crossval": self.perform_crossval,
            "plot": self.plot,
            "preserve_model": self.preserve_model,
            # not yet
            "target_mclf": self.target_mclf,
        }

    def train(self, data):
        data_eng = self.feature_engineering(data)
        train, val, test = self.preprocess_feature(data_eng)
        all_features = self.feature_selection(train)
        std_data, reshaped_data = self.preprocess_model(train, val, test)
        self.model_selection(std_data, reshaped_data)

    def predict(self, new_data):
        data = self.feature_engineering(
            data=new_data,
            for_training=False,
        )
        data = self.preprocess_feature(data, for_training=False)
        data, scaled_data, reshaped_data = self.preprocess_model(
            data, for_training=False
        )

        for target_number in self.target_numbers:

            # loading model
            training_target_dir = f"{self.dataset.path}/TARGET_{target_number}"
            all_features = self.dataset.get_all_features(
                date_column=self.date_column, group_column=self.group_column
            )
            if self.dataset.name == "data_28_X_X":
                features = joblib.load(
                    f"{self.dataset.path}/preprocessing/features_{target_number}.pkl"
                )  # we keep this for backward compatibility
            else:
                features = self.dataset.get_features(target_number)
            model = ModelEngine(path=training_target_dir)
            model.load()

            # getting data
            if model.recurrent:
                features_idx = [
                    i for i, e in enumerate(all_features) if e in set(features)
                ]
                x_pred = reshaped_data[:, :, features_idx]
            else:
                x_pred = scaled_data[features] if model.need_scaling else data[features]

            # predicting
            y_pred = model.predict(x_pred)

            # fix for recurrent model because x_val has no index as it is a 3D np array
            if model.recurrent:
                y_pred.index = (
                    new_data.index
                )  # TODO: not sure this will work for old dataset not aligned with data_for_training for test use case (done, this is why we decode the test set)

            # unscaling prediction
            if (
                model.need_scaling
                and model.target_type == "regression"
                and model.scaler_y is not None
            ):
                y_pred = pd.Series(
                    model.scaler_y.inverse_transform(
                        y_pred.values.reshape(-1, 1)
                    ).flatten(),
                    index=new_data.index,
                )

            # renaming pred column and concatenating with initial data
            if isinstance(y_pred, pd.DataFrame):
                y_pred.rename(
                    columns={"PRED": f"TARGET_{target_number}_PRED"}, inplace=True
                )
                new_data = pd.concat(
                    [new_data, y_pred[f"TARGET_{target_number}_PRED"]], axis=1
                )

            else:
                y_pred.name = f"TARGET_{target_number}_PRED"
                new_data = pd.concat([new_data, y_pred], axis=1)

        return new_data

    def feature_engineering(self, data, for_training=True):
        app = FeatureEngineeringEngine(
            data=data,
            columns_drop=self.columns_drop,
            columns_boolean=self.columns_boolean,
            columns_date=self.columns_date,
            columns_te_groupby=self.columns_te_groupby,
            columns_te_target=self.columns_te_target,
            for_training=for_training,
        )
        data = app.run()
        return data

    def preprocess_feature(self, data, for_training=True):
        app = PreprocessFeature(
            data=data,
            dataset=self.dataset,
            time_series=self.time_series,
            date_column=self.date_column,
            group_column=self.group_column,
            val_size=self.val_size,
            test_size=self.test_size,
            columns_pca=self.columns_pca,
            columns_onehot=self.columns_onehot,
            columns_binary=self.columns_binary,
            columns_frequency=self.columns_frequency,
            columns_ordinal=self.columns_ordinal,
            target_numbers=self.target_numbers,
            target_clf=self.target_clf,
        )
        if for_training:
            train, val, test = app.run()
            return train, val, test
        else:
            data = app.inference()
            return data

    def feature_selection(self, train):
        for target_number in self.target_numbers:
            app = FeatureSelectionEngine(
                train=train,
                target_number=target_number,
                dataset=self.dataset,
                target_clf=self.target_clf,
            )
            app.run()
        self.dataset = Dataset.get(self.dataset.id)
        all_features = self.dataset.get_all_features(
            date_column=self.date_column, group_column=self.group_column
        )
        return all_features

    def preprocess_model(self, train, val=None, test=None, for_training=True):
        app = PreprocessModel(
            train=train,
            val=val,
            test=test,
            dataset=self.dataset,
            target_numbers=self.target_numbers,
            target_clf=self.target_clf,
            models_idx=self.models_idx,
            time_series=self.time_series,
            max_timesteps=self.max_timesteps,
            date_column=self.date_column,
            group_column=self.group_column,
        )
        if for_training:
            data, reshaped_data = app.run()
            return data, reshaped_data
        else:
            data, scaled_data, reshaped_data = app.inference()
            return data, scaled_data, reshaped_data

    def model_selection(self, data, reshaped_data):
        for target_number in self.target_numbers:
            app = ModelSelectionEngine(
                data=data,
                reshaped_data=reshaped_data,
                target_number=target_number,
                dataset=self.dataset,
                target_clf=self.target_clf,
                models_idx=self.models_idx,
                time_series=self.time_series,
                date_column=self.date_column,
                group_column=self.group_column,
            )
            app.run(
                self.session_name,
                perform_hyperopt=self.perform_hyperopt,
                number_of_trials=self.number_of_trials,
                perform_crossval=self.perform_crossval,
                plot=self.plot,
                preserve_model=self.preserve_model,
            )
