#!/bin/bash

# 在后台启动 run-leaderboard
make run-leaderboard &

# 执行 CMD 中的命令
exec "$@"
