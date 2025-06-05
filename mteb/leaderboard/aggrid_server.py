from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有跨域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GET接口，支持URL参数gridOptions
@app.get("/aggrid")
async def aggrid_get(gridOptions: str = None):
    if gridOptions:
        try:
            grid_options = json.loads(gridOptions)
        except Exception:
            grid_options = None
    else:
        grid_options = None
    if grid_options is None:
        # 默认示例
        grid_options = {
            "columnDefs": [
                {"headerName": "模型名称", "field": "模型名称"},
                {"headerName": "参数量", "field": "参数量"},
                {"headerName": "训练数据", "field": "训练数据"},
                {"headerName": "发布时间", "field": "发布时间"},
                {
                    "headerName": "性能评分",
                    "field": "性能评分",
                    "type": "numericColumn",
                },
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
            "paginationPageSizeSelector": [10, 20, 50, 100],
            "domLayout": "autoHeight",
            "animateRows": True,
            "theme": "legacy",
        }
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-grid.css" />
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-theme-alpine.css" />
        <style>
        /* 让分页栏居中 */
        .ag-theme-alpine .ag-paging-panel {{
            justify-content: center !important;
            display: flex !important;
        }}
        </style>
    </head>
    <body>
        <div id="myGrid" class="ag-theme-alpine" style="height: 500px; width: 100%;"></div>
        <script src="https://unpkg.com/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
        <script>
            var gridOptions = {json.dumps(grid_options, ensure_ascii=False)};
            var eGridDiv = document.getElementById('myGrid');
            agGrid.createGrid(eGridDiv, gridOptions);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


# 保留POST接口（可选）
@app.post("/aggrid")
async def aggrid_post(request: Request):
    body = await request.json()
    grid_options = body.get("gridOptions")
    if grid_options is None:
        # 默认示例
        grid_options = {
            "columnDefs": [
                {"headerName": "模型名称", "field": "模型名称"},
                {"headerName": "参数量", "field": "参数量"},
                {"headerName": "训练数据", "field": "训练数据"},
                {"headerName": "发布时间", "field": "发布时间"},
                {
                    "headerName": "性能评分",
                    "field": "性能评分",
                    "type": "numericColumn",
                },
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
            "paginationPageSizeSelector": [10, 20, 50, 100],
            "domLayout": "autoHeight",
            "animateRows": True,
            "theme": "legacy",
        }
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-grid.css" />
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-theme-alpine.css" />
        <style>
        /* 让分页栏居中 */
        .ag-theme-alpine .ag-paging-panel {{
            justify-content: center !important;
            display: flex !important;
        }}
        </style>
    </head>
    <body>
        <div id="myGrid" class="ag-theme-alpine" style="height: 500px; width: 100%;"></div>
        <script src="https://unpkg.com/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
        <script>
            var gridOptions = {json.dumps(grid_options, ensure_ascii=False)};
            var eGridDiv = document.getElementById('myGrid');
            agGrid.createGrid(eGridDiv, gridOptions);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("aggrid_server:app")
