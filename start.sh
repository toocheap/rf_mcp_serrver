#!/bin/bash
#
# 開発環境では
#
# 直接実行
# chmod +x start.sh
# ./start.sh
# または
# uvicorn main:app --reload
#
# 本番環境では
#
# # Dockerを使用
# docker-compose up -d
# または直接Gunicornを使用
# gunicorn -c gunicorn.conf.py main:app
export $(cat .env | xargs)
python main.py
