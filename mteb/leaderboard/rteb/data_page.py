# -*- coding: utf-8 -*-
# @Date     : 2025/2/5 16:26
# @Author   : q275343119
# @File     : data_page.py
# @Description:
import io

import pandas as pd

from mteb.leaderboard.rteb.data_engine import DataEngine

COLUMNS = ['model_name',
           'embd_dtype', 'embd_dim', 'num_params', 'max_tokens', 'similarity',
           'query_instruct', 'corpus_instruct', 'reference'

           ]


def get_closed_dataset(data_engine):
    closed_list = []
    results = data_engine.results
    for result in results:
        if result.get("is_closed"):
            closed_list.append(result.get("dataset_name"))
    return closed_list


def unit_change(x):
    """
    unit change
    Returns:

    """
    if x >= 1e9: return f"{x / 1e9:.2f}B"
    if x >= 1e6: return f"{x / 1e6:.2f}M"
    if x >= 1e3: return f"{x / 1e3:.2f}K"
    return x


def rteb_table_data(group_name, data_engine=None):
    """
    table_area
    :param group_name:
    :param data_engine:
    :return:
    """
    df = data_engine.jsons_to_df().copy()

    # get columns
    column_list = []
    avg_column = None
    if group_name == "Overall":
        avg_columns = []
        for column in df.columns:

            if column.startswith("Average"):
                avg_columns.insert(0, column)
                continue
            if "Average" in column:
                avg_columns.append(column)
                continue
        avg_column = avg_columns[0]
        column_list.extend(avg_columns)
    else:
        for column in df.columns:

            if column.startswith(group_name.capitalize() + " "):
                avg_column = column

                column_list.append(avg_column)

    dataset_list = []
    dataset_name = group_name.lower() if group_name != "Overall" else "text"
    for dataset_dict in data_engine.datasets:
        if dataset_dict["name"] == dataset_name:
            dataset_list = dataset_dict["datasets"]
    if group_name != "Overall":
        column_list.extend(dataset_list)
    closed_list = get_closed_dataset(data_engine)
    close_avg_list = list(set(dataset_list) & set(closed_list))
    df["Closed average"] = df[close_avg_list].mean(axis=1).round(2)
    column_list.append("Closed average")

    open_avg_list = list(set(dataset_list) - set(closed_list))
    df["Open average"] = df[open_avg_list].mean(axis=1).round(2)
    column_list.append("Open average")
    df_detail = df[["model_name"] + dataset_list].rename(columns={"model_name": "Model Name"})
    df = df[COLUMNS + column_list].sort_values(by=avg_column, ascending=False)
    df_reference = df[["model_name","reference"]].rename(columns={"model_name": "Model Name"})
    # rename avg column  name
    if group_name != "Overall":
        new_column = avg_column.replace(group_name.capitalize(), "").strip()
        df.rename(columns={avg_column: new_column}, inplace=True)
        column_list.remove(avg_column)
        avg_column = new_column

    if group_name == "Overall":
        rename_map = {
            "model_name": "Model Name",
            avg_column: "Overall Score",
            "Open average": "Open Average",
            "Closed average": "Closed Average",
            "embd_dtype": "Embd Dtype",
            "embd_dim": "Embd Dim",
            "num_params": "Number of Parameters",
            "max_tokens": "Context Length",
            **{column: column if "Average" not in column else column.replace("Average", "").strip().capitalize() for
               column in column_list if column not in (avg_column, "Closed average", "Open average")}
        }
    else:
        rename_map = {
            "model_name": "Model Name",
            avg_column: "Overall Score",
            "Open average": "Open Average",
            "Closed average": "Closed Average",
            "embd_dtype": "Embd Dtype",
            "embd_dim": "Embd Dim",
            "num_params": "Number of Parameters",
            "max_tokens": "Context Length",
            **{column: column for
               column in column_list if column not in (avg_column, "Closed average", "Open average")}
        }

    df.rename(columns=rename_map, inplace=True)
    df["Number of Parameters"] = df["Number of Parameters"].apply(lambda x: unit_change(x))
    df = df.map(lambda x: "Unknown" if pd.isnull(x) else x)

    return df[list(rename_map.values())], df_detail,df_reference
