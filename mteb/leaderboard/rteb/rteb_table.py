from __future__ import annotations
from __future__ import annotations

import math
import re
from collections import defaultdict

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from pandas.api.types import is_numeric_dtype

from mteb.models.overview import get_model_meta
from mteb.overview import get_task, get_tasks


def create_light_green_cmap():
    cmap = plt.cm.get_cmap("Greens")
    num_colors = 256
    half_colors = np.linspace(0, 0.5, num_colors)
    half_cmap = [cmap(val) for val in half_colors]
    light_green_cmap = LinearSegmentedColormap.from_list(
        "LightGreens", half_cmap, N=256
    )
    return light_green_cmap


def get_column_widths(df: pd.DataFrame) -> list[str]:
    # Please do not remove this function when refactoring.
    # Column width calculation seeminlgy changes regularly with Gradio releases,
    # and this piece of logic is good enough to quickly fix related issues.
    widths = []
    for column_name in df.columns:
        column_word_lengths = [len(word) for word in column_name.split()]
        if is_numeric_dtype(df[column_name]):
            value_lengths = [len(f"{value:.2f}") for value in df[column_name]]
        else:
            value_lengths = [len(str(value)) for value in df[column_name]]
        max_length = max(max(column_word_lengths), max(value_lengths))
        n_pixels = 25 + (max_length * 10)
        widths.append(f"{n_pixels}px")
    return widths


def rteb_apply_styling(
        joint_table: pd.DataFrame,
        per_task: pd.DataFrame,

) -> tuple[gr.DataFrame, gr.DataFrame]:
    excluded_columns = ['Model Name', 'Overall Score', 'Open Average', 'Closed Average',
                        'Embd Dtype', 'Embd Dim', 'Number of Parameters', 'Context Length', 'Average', 'Model']
    gradient_columns = [
        col for col in joint_table.columns if col not in excluded_columns
    ]

    score_columns = gradient_columns

    light_green_cmap = create_light_green_cmap()
    numeric_data = joint_table.copy()

    joint_table_style = joint_table.style.format(
        {
            **dict.fromkeys(score_columns, "{:.2f}")
        },
        na_rep="",
    )
    joint_table_style = joint_table_style.highlight_max(subset=score_columns, props="font-weight: bold")

    # Apply background gradients for each selected column
    for col in gradient_columns:
        if col in joint_table.columns:
            mask = numeric_data[col].notna()
            if col != "Zero-shot":
                gmap_values = numeric_data[col] * 100
                cmap = light_green_cmap
                joint_table_style = joint_table_style.background_gradient(
                    cmap=cmap,
                    subset=pd.IndexSlice[mask, col],
                    gmap=gmap_values.loc[mask],
                )
            else:
                gmap_values = numeric_data[col]
                cmap = "RdYlGn"
                joint_table_style = joint_table_style.background_gradient(
                    cmap=cmap,
                    subset=pd.IndexSlice[mask, col],
                    vmin=50,
                    vmax=100,
                    gmap=gmap_values.loc[mask],
                )
    task_score_columns = per_task.select_dtypes("number").columns

    per_task_style = per_task.style.format(
        "{:.2f}", subset=task_score_columns, na_rep=""
    ).highlight_max(subset=task_score_columns, props="font-weight: bold")
    # TODO: uncomment this when Gradio fixes it.
    # The fix is already merged and contained in this release: https://github.com/gradio-app/gradio/pull/11032
    # It will be available in Gradio 5.25.3
    # for col in task_score_columns:
    #     if col != "Model":
    #         mask = per_task[col].notna()
    #         per_task_style = per_task_style.background_gradient(
    #             cmap=light_green_cmap,
    #             subset=pd.IndexSlice[mask, col],
    #             gmap=per_task[col].loc[mask],
    #         )
    column_widths = get_column_widths(joint_table_style.data)
    column_widths[0] = "100px"
    column_widths[1] = "250px"
    return (
        gr.DataFrame(
            joint_table_style,
            interactive=False,
            pinned_columns=1,
            column_widths=column_widths,
            wrap=True,
            show_fullscreen_button=True,
            show_copy_button=True,
            show_search="filter",
        ),
        gr.DataFrame(
            per_task_style,
            interactive=False,
            pinned_columns=1,
            show_fullscreen_button=True,
            show_copy_button=True,
            show_search="filter",
        ),
    )
