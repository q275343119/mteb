# -*- coding: utf-8 -*-
# @Date     : 2025/4/21 10:51
# @Author   : q275343119
# @File     : multi_app_tabs.py
# @Description: 使用 Tabs 替代 Sidebar 实现页面切换

import gradio as gr

def multi_app_with_tabs() -> gr.Blocks:
    with gr.Blocks(
        fill_width=True,
        theme=gr.themes.Soft(
            font=[gr.themes.GoogleFont("Roboto Mono"), "Arial", "sans-serif"],
        ),
    ) as demo:
        with gr.Tabs():
            with gr.TabItem("MTEB-LEADERBOARD"):
                gr.HTML("""
                    <iframe src="/sub/"
                            style="width: 100%; height: 90vh; border: none;" scrolling="auto">
                    </iframe>
                """)
            with gr.TabItem("Retrieval Embedding Benchmark"):
                gr.HTML("""
                    <iframe src="https://embedding-benchmark-rteb.hf.space/"
                            style="width: 100%; height: 90vh; border: none;" scrolling="auto">
                    </iframe>
                """)

    return demo


if __name__ == '__main__':
    app = multi_app_with_tabs()
    app.launch(server_name="0.0.0.0", server_port=7861)
