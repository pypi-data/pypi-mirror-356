import pandas as pd
import os
from pathlib import Path

os.environ["COVERAGE_FILE"] = str(Path(".coverage").resolve())

# Internal
from lecrapaud.directories import tmp_dir
from lecrapaud.utils import logger
from lecrapaud.config import PYTHON_ENV
from lecrapaud.db import (
    Dataset,
    Target,
)
from lecrapaud.db.session import get_db


def create_dataset(
    data: pd.DataFrame,
    corr_threshold,
    percentile,
    max_features,
    date_column,
    group_column,
    **kwargs,
):
    dates = {}
    if date_column:
        dates["start_date"] = pd.to_datetime(data[date_column].iat[0])
        dates["end_date"] = pd.to_datetime(data[date_column].iat[-1])

    groups = {}
    if group_column:
        groups["number_of_groups"] = data[group_column].nunique()
        groups["list_of_groups"] = data[group_column].unique().tolist()

    with get_db() as db:
        all_targets = Target.get_all(db=db)
        targets = [target for target in all_targets if target.name in data.columns]
        dataset_name = f"data_{groups["number_of_groups"] if group_column else 'ng'}_{corr_threshold}_{percentile}_{max_features}_{dates['start_date'].date() if date_column else 'nd'}_{dates['end_date'].date() if date_column else 'nd'}"

        dataset_dir = f"{tmp_dir}/{dataset_name}"
        preprocessing_dir = f"{dataset_dir}/preprocessing"
        data_dir = f"{dataset_dir}/data"
        os.makedirs(dataset_dir, exist_ok=True)
        os.makedirs(preprocessing_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)

        dataset = Dataset.upsert(
            match_fields=["name"],
            db=db,
            name=dataset_name,
            path=Path(dataset_dir).resolve(),
            type="training",
            size=data.shape[0],
            corr_threshold=corr_threshold,
            percentile=percentile,
            max_features=max_features,
            **groups,
            **dates,
            targets=targets,
        )

        return dataset
