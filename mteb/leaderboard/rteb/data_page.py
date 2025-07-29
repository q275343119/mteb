# -*- coding: utf-8 -*-
# @Date     : 2025/2/5 16:26
# @Author   : q275343119
# @File     : data_page.py
# @Description:
import io

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


def table_area(group_name, data_engine=None):
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

    df = df[COLUMNS + column_list].sort_values(by=avg_column, ascending=False)

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

    return df[list(rename_map.values())]

if __name__ == '__main__':
    data_engine = DataEngine()
    df = table_area("Overall",data_engine)
    print(df)

    df = table_area("Code",data_engine)
    print(df)