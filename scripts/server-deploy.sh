#!/bin/bash
set -e

echo "=== 腾讯云服务器端部署脚本 ==="

PROJECT_DIR="/www/base-room"
DEPLOY_DIR="$PROJECT_DIR/deploy"

# 确保目录存在
mkdir -p $PROJECT_DIR

# 如果这是首次部署，从 GitHub 拉取代码（可选）
# git clone https://github.com/你的用户名/base-room.git $PROJECT_DIR

cd $DEPLOY_DIR

# 复制 .env 配置文件（首次部署前需手动创建）
if [ ! -f "$PROJECT_DIR/base-back/.env" ]; then
  echo "警告：未找到 .env 文件，请根据 .env.example 创建"
fi

# 停止并重建容器
docker-compose down
docker-compose up -d --build

# 清理旧镜像和悬空层
docker image prune -f
docker system prune -f --volumes

echo "=== 部署完成 ==="
echo "访问地址: http://$TENCENT_HOST"