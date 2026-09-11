#!/bin/bash
set -e
echo "=== My Project 部署开始 ==="
cd "$(dirname "$0")"
docker-compose down
docker-compose up -d --build
docker image prune -f
echo "=== 部署完成 ==="
echo "官网  web-pc    : http://www.base-room.cn/"
echo "后台  web-front : http://www.base-room.cn/admin/"
echo "接口  web-back  : http://www.base-room.cn/api/health"
echo "账号 / 密码     : admin / 123456"