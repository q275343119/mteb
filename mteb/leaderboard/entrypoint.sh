#!/bin/bash

# 启动子服务（8080），比如 leaderboard_sub.py
python -m mteb.leaderboard.app &

# 启动主服务（7860），比如 leaderboard_main.py
python -m mteb.leaderboard.multi_app &

# 启动 nginx（前台）
nginx -c /mteb/nginx.conf -g "daemon off;"

