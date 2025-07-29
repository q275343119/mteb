"""
Data service provider
"""
import json
from typing import List

import pandas as pd

from .utils.cache_decorator import cache_df_with_custom_key, cache_dict_with_custom_key
from .utils.http_utils import get

COLUMNS = ['model_name',
           'embd_dtype', 'embd_dim', 'num_params', 'max_tokens', 'similarity',
           'query_instruct', 'corpus_instruct',

           ]
COLUMNS_TYPES = ["markdown",
                 'str', 'str', 'number', 'number', 'str',
                 'str', 'str',

                 ]

BRANCH = 'main'
GIT_URL = f"https://raw.githubusercontent.com/embedding-benchmark/rteb/refs/heads/{BRANCH}/results/"
DATASET_URL = f"{GIT_URL}datasets.json"
MODEL_URL = f"{GIT_URL}models.json"
RESULT_URL = f"{GIT_URL}results.json"


class DataEngine:

    def __init__(self):
        self.df = self.init_dataframe()

    @property
    @cache_dict_with_custom_key("models")
    def models(self):
        """
        Get models data
        """
        res = get(MODEL_URL)
        if res.status_code == 200:
            return res.json()
        return {}

    @property
    @cache_dict_with_custom_key("datasets")
    def datasets(self):
        """
        Get tasks data
        """
        res = get(DATASET_URL)
        if res.status_code == 200:
            return res.json()
        return {}

    @property
    @cache_dict_with_custom_key("results")
    def results(self):
        """
        Get results data
        """
        res = get(RESULT_URL)
        if res.status_code == 200:
            return res.json()
        return {}

    def init_dataframe(self):
        """
        Initialize DataFrame
        """
        d = {"hello": [123], "world": [456]}
        return pd.DataFrame(d)

    @cache_df_with_custom_key("json_result")
    def jsons_to_df(self):

        results_list = self.results
        df_results_list = []
        for result_dict in results_list:
            dataset_name = result_dict["dataset_name"]
            df_result_row = pd.DataFrame(result_dict["results"])
            df_result_row["dataset_name"] = dataset_name
            df_results_list.append(df_result_row)
        df_result = pd.concat(df_results_list)

        df_result = df_result[["model_name", "dataset_name", "ndcg_at_10", "embd_dim", "embd_dtype"]]

        df_result["ndcg_at_10"] = (df_result["ndcg_at_10"] * 100).round(2)

        df_datasets_list = []
        for item in self.datasets:
            dataset_names = item["datasets"]
            df_dataset_row = pd.DataFrame(
                {
                    "group_name": [item["name"] for _ in range(len(dataset_names))],
                    "dataset_name": dataset_names,
                    "leaderboard": [item["leaderboard"] for _ in range(len(dataset_names))]
                }
            )
            df_datasets_list.append(df_dataset_row)
        df_dataset = pd.concat(df_datasets_list).drop_duplicates()

        models_list = self.models

        df_model = pd.DataFrame(models_list)

        # Create mapping for model names/aliases
        if 'alias' in df_model.columns:
            # Create a lookup table for alias to model_name mapping
            alias_mapping = df_model[df_model['alias'].notna()].set_index('alias')['model_name'].to_dict()

            # Add rows for aliases to enable joining
            alias_rows = []
            for _, row in df_model[df_model['alias'].notna()].iterrows():
                alias_row = row.copy()
                alias_row['model_name'] = row['alias']
                alias_rows.append(alias_row)

            if alias_rows:
                df_model_extended = pd.concat([df_model, pd.DataFrame(alias_rows)], ignore_index=True)
            else:
                df_model_extended = df_model
        else:
            df_model_extended = df_model

        df = pd.merge(df_result, df_dataset, on=["dataset_name"], how="inner")

        # set dataset default value to 0
        df = df.pivot(index=["model_name", "embd_dim", "embd_dtype", "group_name"], columns="dataset_name",
                 values=["ndcg_at_10"]).fillna(0).stack(level=1).reset_index()
        df = pd.merge(df, df_dataset, on=["group_name","dataset_name"], how="inner")

        # dataset_num_map = {}
        # grouped_dataset_count = df.groupby(["group_name"]).agg({
        #     "dataset_name": "nunique"
        # }).reset_index()
        #
        # for _, row in grouped_dataset_count.iterrows():
        #     dataset_num_map[row["group_name"]] = row["dataset_name"]

        grouped_model = df.groupby(["model_name", "group_name", "embd_dim", "embd_dtype"]).agg({
            "ndcg_at_10": "mean",
        }).reset_index()

        pivot = grouped_model.pivot(index=["model_name", "embd_dim", "embd_dtype"], columns="group_name",
                                    values=["ndcg_at_10"]).round(2).fillna(0)

        # Rename columns
        pivot.columns = list(
            map(lambda x: f"{x[1].capitalize()} Average" if x[1] != 'text' else f"Average", pivot.columns))

        pivot_dataset = df_result.pivot(index=["model_name", "embd_dim", "embd_dtype"], columns="dataset_name", values="ndcg_at_10").fillna(0)

        df = pd.merge(df_model_extended, pivot, on=["model_name", "embd_dim", "embd_dtype"])
        df = pd.merge(df, pivot_dataset, on=["model_name", "embd_dim", "embd_dtype"])

        if df.empty:
            return pd.DataFrame(columns=COLUMNS + ["reference"])
        return df

    def filter_df(self, group_name: str):
        """
        filter_by_providers
        """
        df = self.jsons_to_df()

        return df[df["group_name"] == group_name][COLUMNS][:]
