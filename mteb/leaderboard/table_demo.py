import gradio as gr
import urllib.parse
import json


def get_aggrid_iframe():
    grid_options = {
        "columnDefs": [
            {"headerName": "模型名称", "field": "模型名称"},
            {"headerName": "参数量", "field": "参数量"},
            {"headerName": "训练数据", "field": "训练数据"},
            {"headerName": "发布时间", "field": "发布时间"},
            {"headerName": "性能评分", "field": "性能评分", "type": "numericColumn"},
        ],
        "rowData": [
            {
                "模型名称": "BERT",
                "参数量": "110M",
                "训练数据": "BookCorpus + Wikipedia",
                "发布时间": "2018",
                "性能评分": 0.85,
            },
            {
                "模型名称": "RoBERTa",
                "参数量": "355M",
                "训练数据": "BookCorpus + Wikipedia",
                "发布时间": "2019",
                "性能评分": 0.87,
            },
            {
                "模型名称": "GPT-2",
                "参数量": "1.5B",
                "训练数据": "WebText",
                "发布时间": "2019",
                "性能评分": 0.89,
            },
            {
                "模型名称": "T5",
                "参数量": "11B",
                "训练数据": "C4",
                "发布时间": "2020",
                "性能评分": 0.92,
            },
        ],
        "defaultColDef": {
            "sortable": True,
            "filter": True,
            "resizable": True,
        },
        "pagination": True,
        "paginationPageSize": 10,
        "domLayout": "autoHeight",
        "animateRows": True,
    }
    grid_options_str = urllib.parse.quote(json.dumps(grid_options, ensure_ascii=False))
    url = f"http://localhost:8000/aggrid?gridOptions={grid_options_str}"
    return f'<iframe src="{url}" width="100%" height="600" frameborder="0"></iframe>'


with gr.Blocks(title="AG Grid via FastAPI") as demo:
    gr.Markdown("# AG Grid（通过 FastAPI 渲染，iframe方式）")
    gr.HTML(get_aggrid_iframe())

if __name__ == "__main__":
    demo.launch()
