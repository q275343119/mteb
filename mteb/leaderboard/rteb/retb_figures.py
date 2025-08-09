import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from mteb.leaderboard.rteb.data_engine import DataEngine
from mteb.leaderboard.rteb.data_page import rteb_table_data

default_column = ['Model Name', 'Overall Score', 'Open Average', 'Closed Average',
                  'Embd Dtype', 'Embd Dim', 'Number of Parameters', 'Context Length', 'Average', 'Model']

TOP_N = 5

line_colors = [
    "#EE4266",
    "#00a6ed",
    "#ECA72C",
    "#B42318",
    "#3CBBB1",
]


def parse_n_params(text: str) -> int:
    if text.endswith("M"):
        return float(text[:-1]) * 1e6
    if text.endswith("B"):
        return float(text[:-1]) * 1e9
    else:
        return np.nan


def process_max_tokens(x):
    if pd.isna(x):
        return "Unknown"
    if np.isinf(x):
        return "Infinite"
    return str(int(x))


def add_size_guide(fig: go.Figure):
    xpos = [2 * 1e6] * 4
    ypos = [7.8, 8.5, 9, 10]
    sizes = [256, 1024, 2048, 4096]
    fig.add_trace(
        go.Scatter(
            showlegend=False,
            opacity=0.3,
            mode="markers",
            marker=dict(
                size=np.sqrt(sizes),
                color="rgba(0,0,0,0)",
                line=dict(color="black", width=2),
            ),
            x=xpos,
            y=ypos,
        )
    )
    fig.add_annotation(
        text="<b>Embedding Size</b>",
        font=dict(size=16),
        x=np.log10(10 * 1e6),
        y=10,
        showarrow=False,
        opacity=0.3,
    )
    return fig


def text_plot(text: str):
    """Returns empty scatter plot with text added, this can be great for error messages."""
    return px.scatter(template="plotly_white").add_annotation(
        text=text, showarrow=False, font=dict(size=20)
    )


def failsafe_plot(fun):
    """Decorator that turns the function producing a figure failsafe.
    This is necessary, because once a Callback encounters an exception it
    becomes useless in Gradio.
    """

    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            return text_plot(f"Couldn't produce plot. Reason: {e}")

    return wrapper


@failsafe_plot
def rteb_performance_size_plot(df_summary: pd.DataFrame, df_detail: pd.DataFrame) -> go.Figure:
    df_performance = df_detail.set_index(["Model Name"]).mean(axis=1).reset_index()
    df_performance.columns = ["Model Name", "Mean (Task)"]
    df_model = df_summary[["Model Name", "Embd Dim", "Number of Parameters", "Context Length"]]
    df_performance = pd.merge(df_performance, df_model, on="Model Name", how="left")
    df_performance["Number of Parameters"] = df_performance["Number of Parameters"].map(parse_n_params)
    df_performance["Model"] = df_performance["Model Name"]
    df_performance["model_text"] = df_performance["Model"]
    df_performance["Embedding Dimensions"] = df_performance["Embd Dim"]
    df_performance["Max Tokens"] = df_performance["Context Length"]
    df_performance["Model"] = df_performance["Model"]
    df_performance["Log(Tokens)"] = np.log10(df_performance["Max Tokens"])

    df = df_performance.dropna(
        subset=["Mean (Task)", "Number of Parameters", "Embedding Dimensions"]
    )
    # if not len(df.index):
    #     return go.Figure()

    min_score, max_score = df["Mean (Task)"].min(), df["Mean (Task)"].max()
    df["sqrt(dim)"] = np.sqrt(df["Embedding Dimensions"])
    df["Max Tokens"] = df["Max Tokens"].apply(lambda x: process_max_tokens(x))
    fig = px.scatter(
        df,
        x="Number of Parameters",
        y="Mean (Task)",
        log_x=True,
        template="plotly_white",
        text="model_text",
        size="sqrt(dim)",
        color="Log(Tokens)",
        range_color=[2, 5],
        range_y=[min(0, min_score * 1.25), max_score * 1.25],
        hover_data={
            "Max Tokens": True,
            "Embedding Dimensions": True,
            "Number of Parameters": True,
            "Mean (Task)": True,
            # TODO what is Rank (Borda)
            # "Rank (Borda)": True,
            "Log(Tokens)": False,
            "sqrt(dim)": False,
            "model_text": False,
        },
        hover_name="Model",
        color_continuous_scale=px.colors.sequential.Greens,
    )
    # Note: it's important that this comes before setting the size mode
    fig = add_size_guide(fig)
    fig.update_traces(
        marker=dict(
            sizemode="diameter",
            sizeref=1.5,
            sizemin=0,
        )
    )
    fig.add_annotation(x=1e9, y=10, text="Model size:")
    fig.update_layout(
        coloraxis_colorbar=dict(  # noqa
            title="Max Tokens",
            tickvals=[2, 3, 4, 5],
            ticktext=[
                "100",
                "1K",
                "10K",
                "100K",
            ],
        ),
        hoverlabel=dict(  # noqa
            bgcolor="white",
            font_size=16,
        ),
    )
    fig.update_traces(
        textposition="top center",
    )
    fig.update_layout(
        font=dict(size=16, color="black"),  # noqa
        margin=dict(b=20, t=10, l=20, r=10),  # noqa
    )
    return fig


@failsafe_plot
def rteb_radar_chart(df: pd.DataFrame) -> go.Figure:
    df = df.copy().rename(columns={"Model Name": "Model"}) if "Model" not in df.columns else df.copy()

    # Remove whitespace
    task_type_columns = [
        column for column in df.columns if column not in default_column
    ]
    if len(task_type_columns) <= 1:
        raise ValueError(
            "Couldn't produce radar chart, the benchmark only contains one task category."
        )
    df = df[["Model", *task_type_columns]].set_index("Model")
    df = df.mask(df == "", np.nan)
    df = df.dropna()
    df = df.head(TOP_N)
    df = df.iloc[::-1]
    fig = go.Figure()
    for i, (model_name, row) in enumerate(df.iterrows()):
        fig.add_trace(
            go.Scatterpolar(
                name=model_name,
                r=[row[task_type] for task_type in task_type_columns]
                  + [row[task_type_columns[0]]],
                theta=task_type_columns + [task_type_columns[0]],
                showlegend=True,
                mode="lines",
                line=dict(width=2, color=line_colors[i]),
                fill="toself",
                fillcolor="rgba(0,0,0,0)",
            )
        )
    fig.update_layout(
        font=dict(size=13, color="black"),  # noqa
        template="plotly_white",
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor="black",
                linecolor="rgba(0,0,0,0)",
                gridwidth=1,
                showticklabels=False,
                ticks="",
            ),
            angularaxis=dict(
                gridcolor="black", gridwidth=1.5, linecolor="rgba(0,0,0,0)"
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.4,
            itemwidth=30,
            font=dict(size=13),
            entrywidth=0.6,
            entrywidthmode="fraction",
        ),
        margin=dict(l=0, r=16, t=30, b=30),
        autosize=True,
    )
    return fig
