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
        .ag-theme-alpine .ag-paging-panel .ag-theme-streamlit {{
            justify-content: center !important;
            display: flex !important;

        }}
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
.ag-theme-alpine, .ag-theme-streamlit {{
    --ag-background-color: #fff;
    --ag-foreground-color: #181d1f;
    --ag-subheader-background-color: #fff;
    --ag-alpine-active-color: #2196f3;
    --ag-range-selection-border-color: #2196f3;
    --ag-subheader-toolbar-background-color: hsla(0,0%,100%,.5);
    --ag-selected-row-background-color: rgba(33,150,243,.1);
    --ag-row-hover-color: rgba(33,150,243,.1);
    --ag-column-hover-color: rgba(33,150,243,.1);
    --ag-chip-background-color: rgba(24,29,31,.07);
    --ag-disabled-foreground-color: rgba(24,29,31,.5);
    --ag-input-focus-border-color: rgba(33,150,243,.4);
    --ag-modal-overlay-background-color: hsla(0,0%,100%,.66);
    --ag-range-selection-background-color: rgba(33,150,243,.2);
    --ag-range-selection-background-color-2: rgba(33,150,243,.36);
    --ag-range-selection-background-color-3: rgba(33,150,243,.488);
    --ag-range-selection-background-color-4: rgba(33,150,243,.59);
    --ag-border-color: rgba(24,29,31,.25);
    --ag-header-column-separator-color: rgba(24,29,31,.125);
    --ag-header-column-resize-handle-color: rgba(24,29,31,.125);
}}

.ag-theme-alpine, .ag-theme-alpine-auto-dark, .ag-theme-alpine-dark, .ag-theme-streamlit, .ag-theme-streamlit-dark {{
    --ag-alpine-active-color: #2196f3;
    --ag-selected-row-background-color: rgba(33,150,243,.3);
    --ag-row-hover-color: rgba(33,150,243,.1);
    --ag-column-hover-color: rgba(33,150,243,.1);
    --ag-input-focus-border-color: rgba(33,150,243,.4);
    --ag-range-selection-background-color: rgba(33,150,243,.2);
    --ag-range-selection-background-color-2: rgba(33,150,243,.36);
    --ag-range-selection-background-color-3: rgba(33,150,243,.49);
    --ag-range-selection-background-color-4: rgba(33,150,243,.59);
    --ag-background-color: #fff;
    --ag-foreground-color: #181d1f;
    --ag-border-color: #babfc7;
    --ag-secondary-border-color: #dde2eb;
    --ag-header-background-color: #f8f8f8;
    --ag-tooltip-background-color: #f8f8f8;
    --ag-odd-row-background-color: #fcfcfc;
    --ag-control-panel-background-color: #f8f8f8;
    --ag-subheader-background-color: #fff;
    --ag-invalid-color: #e02525;
    --ag-checkbox-unchecked-color: #999;
    --ag-advanced-filter-join-pill-color: #f08e8d;
    --ag-advanced-filter-column-pill-color: #a6e194;
    --ag-advanced-filter-option-pill-color: #f3c08b;
    --ag-advanced-filter-value-pill-color: #85c0e4;
    --ag-checkbox-background-color: var(--ag-background-color);
    --ag-checkbox-checked-color: var(--ag-alpine-active-color);
    --ag-range-selection-border-color: var(--ag-alpine-active-color);
    --ag-secondary-foreground-color: var(--ag-foreground-color);
    --ag-input-border-color: var(--ag-border-color);
    --ag-input-border-color-invalid: var(--ag-invalid-color);
    --ag-input-focus-box-shadow: 0 0 2px 0.1rem var(--ag-input-focus-border-color);
    --ag-panel-background-color: var(--ag-header-background-color);
    --ag-menu-background-color: var(--ag-header-background-color);
    --ag-disabled-foreground-color: rgba(24,29,31,.5);
    --ag-chip-background-color: rgba(24,29,31,.07);
    --ag-input-disabled-border-color: rgba(186,191,199,.3);
    --ag-input-disabled-background-color: rgba(186,191,199,.15);
    --ag-borders: solid 1px;
    --ag-border-radius: 3px;
    --ag-borders-side-button: none;
    --ag-side-button-selected-background-color: transparent;
    --ag-header-column-resize-handle-display: block;
    --ag-header-column-resize-handle-width: 2px;
    --ag-header-column-resize-handle-height: 30%;
    --ag-grid-size: 6px;
    --ag-icon-size: 16px;
    --ag-row-height: calc(var(--ag-grid-size)*7);
    --ag-header-height: calc(var(--ag-grid-size)*8);
    --ag-list-item-height: calc(var(--ag-grid-size)*4);
    --ag-column-select-indent-size: var(--ag-icon-size);
    --ag-set-filter-indent-size: var(--ag-icon-size);
    --ag-advanced-filter-builder-indent-size: calc(var(--ag-icon-size) + var(--ag-grid-size)*2);
    --ag-cell-horizontal-padding: calc(var(--ag-grid-size)*3);
    --ag-cell-widget-spacing: calc(var(--ag-grid-size)*2);
    --ag-widget-container-vertical-padding: calc(var(--ag-grid-size)*2);
    --ag-widget-container-horizontal-padding: calc(var(--ag-grid-size)*2);
    --ag-widget-vertical-spacing: calc(var(--ag-grid-size)*1.5);
    --ag-toggle-button-height: 18px;
    --ag-toggle-button-width: 28px;
    --ag-font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
    --ag-font-size: 13px;
    --ag-icon-font-family: agGridAlpine;
    --ag-selected-tab-underline-color: var(--ag-alpine-active-color);
    --ag-selected-tab-underline-width: 2px;
    --ag-selected-tab-underline-transition-speed: 0.3s;
    --ag-tab-min-width: 240px;
    --ag-card-shadow: 0 1px 4px 1px rgba(186,191,199,.4);
    --ag-popup-shadow: var(--ag-card-shadow);
    --ag-side-bar-panel-width: 250px;
}}
        </style>

    </head>
    <body>
        <div id="myGrid" class="ag-theme-streamlit" style="height: 500px; width: 100%;"></div>
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
