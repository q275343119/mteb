# -*- coding: utf-8 -*-
# @Date     : 2025/4/21 10:51
# @Author   : q275343119
# @File     : multi_app.py
# @Description:

import gradio as gr
def multi_app()-> gr.Blocks:
    with gr.Blocks(
            fill_width=True,
            theme=gr.themes.Soft(
                font=[gr.themes.GoogleFont("Roboto Mono"), "Arial", "sans-serif"],
            ),
    ) as demo:
        # 左侧 Sidebar 导航栏
        with gr.Sidebar():
            gr.Markdown("## 页面导航")
            page_selector = gr.Radio(
                ["mteb-leaderboard".upper(), "Retrieval Embedding Benchmark"],
                label="Page Selector",
                value="mteb-leaderboard".upper(),
            )

        # 主页面区域
        main_container = gr.HTML(visible=True)
        streamlit_iframe = gr.HTML(visible=False)

        # 朋友项目部分
        main_container_html = """
         <iframe src="http://127.0.0.1:7860/"
                       style="width: 100%; height: 90vh; border: none;" scrolling="auto">
               </iframe>
        """
        main_container.value = main_container_html
        # 你的 streamlit 项目 iframe
        iframe_html = """
               <iframe src="https://embedding-benchmark-rteb.hf.space/"
                       style="width: 100%; height: 90vh; border: none;" scrolling="auto">
               </iframe>
               """
        streamlit_iframe.value = iframe_html

        # 页面切换函数
        def toggle_page(page):
            return (
                gr.update(visible=(page == "mteb-leaderboard".upper())),
                gr.update(visible=(page == "Retrieval Embedding Benchmark"))
            )

        page_selector.change(
            fn=toggle_page,
            inputs=page_selector,
            outputs=[main_container, streamlit_iframe]
        )

    return app

if __name__ == '__main__':
    app = multi_app()
    app.launch(server_name="0.0.0.0", server_port=8080)