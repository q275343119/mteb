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
                {"headerName": "模型名称", "field": "模型名称", "suppressMenu": False},
                {"headerName": "参数量", "field": "参数量", "suppressMenu": False},
                {"headerName": "训练数据", "field": "训练数据", "suppressMenu": False},
                {"headerName": "发布时间", "field": "发布时间", "suppressMenu": False},
                {
                    "headerName": "性能评分",
                    "field": "性能评分",
                    "type": "numericColumn",
                    "suppressMenu": False
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
          "filter": True,
          "sortable": True,
          "resizable": True,
          "suppressMenu": False,
        },
            "pagination": True,
            "paginationPageSize": 10,
            "paginationPageSizeSelector": [10, 20, 50, 100],
            "domLayout": "autoHeight",
            "animateRows": True,
            "theme": "legacy",
        }
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>AG Grid - Streamlit Theme</title>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-balham.css"
  />
  <style>
    .ag-theme-streamlit {{
      --ag-background-color: #fff;
      --ag-odd-row-background-color: #fff;
      --ag-foreground-color: #31333f;
      --ag-alpine-active-color: #ff4b4b;
      --ag-grid-size: 4px;
      --ag-header-background-color: #f8f9fb;
      --ag-borders: solid 0.5px;
      --ag-border-color: #eaeaeb;
      --ag-cell-horizontal-border: solid #eaeaeb;
      --ag-header-foreground-color: #7f838a;
      --ag-font-family: "Source Sans Pro";
      --ag-font-size: 9.5pt;
      --ag-subheader-background-color: #fff;
      --ag-range-selection-border-color: #ff4b4b;
      --ag-subheader-toolbar-background-color: hsla(0,0%,100%,.5);
      --ag-selected-row-background-color: rgba(255,75,75,.1);
      --ag-row-hover-color: rgba(255,75,75,.1);
      --ag-column-hover-color: rgba(255,75,75,.1);
      --ag-chip-background-color: rgba(49,51,63,.07);
      --ag-input-disabled-background-color: hsla(240,2%,92%,.15);
      --ag-input-disabled-border-color: hsla(240,2%,92%,.3);
      --ag-disabled-foreground-color: rgba(49,51,63,.5);
      --ag-input-focus-border-color: rgba(255,75,75,.4);
      --ag-modal-overlay-background-color: hsla(0,0%,100%,.66);
      --ag-range-selection-background-color: rgba(255,75,75,.2);
      --ag-range-selection-background-color-2: rgba(255,75,75,.36);
      --ag-range-selection-background-color-3: rgba(255,75,75,.488);
      --ag-range-selection-background-color-4: rgba(255,75,75,.59);
      --ag-header-column-separator-color: hsla(240,2%,92%,.5);
      --ag-header-column-resize-handle-color: hsla(240,2%,92%,.5);

    }}
    /* Hover 显示筛选按钮 */
.ag-header-cell-menu-button:not(.ag-header-menu-always-show) {{
    opacity: 0;
    transition: opacity .2s;
}}
.ag-floating-filter-button-button, .ag-header-cell-filter-button, .ag-header-cell-menu-button, .ag-panel-title-bar-button, .ag-side-button-button {{
    cursor: pointer;
}}

.ag-icon {{
    display: block;
    speak: none;
}}

.ag-icon-menu {{
    color: var(--ag-icon-font-color-menu,var(--ag-icon-font-color));
    font-family: var(--ag-icon-font-family-menu,var(--ag-icon-font-family));
    font-weight: var(--ag-icon-font-weight-menu,var(--ag-icon-font-weight));
}}

.ag-icon {{
    color: var(--ag-icon-font-color);
    font-family: var(--ag-icon-font-family);
    font-feature-settings: normal;
    font-size: var(--ag-icon-size);
    font-style: normal;
    font-variant: normal;
    font-weight: var(--ag-icon-font-weight);
    line-height: var(--ag-icon-size);
    text-transform: none;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: var(--ag-icon-size);
    position: relative;
    width: var(--ag-icon-size);
}}
  </style>
</head>
<body>
  <div id="myGrid" class="ag-theme-balham ag-theme-streamlit" style="height: 500px; width: 100%;"></div>

  <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
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
