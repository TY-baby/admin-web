#!/bin/bash
set -e
echo "=== 下线 admin-web (base-room) 部署 ==="
if [ -d /www/base-room ]; then
  echo "[1/3] 停止 /www/base-room 容器..."
  cd /www/base-room
  docker-compose down || true
else
  echo "[1/3] 未找到 /www/base-room，跳过"
fi
echo "[2/3] 清理残留容器..."
docker rm -f base-room-frontend base-room-backend base-room-mysql 2>/dev/null || true
echo "[3/3] 清理悬空镜像..."
docker image prune -f
echo "=== admin-web 已下线，端口 80/3000/3306 已释放 ==="
echo "彻底清除数据: cd /www/base-room && docker-compose down -v"