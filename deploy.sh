#!/bin/bash
# hytf 一键部署脚本
# 用法: ./deploy.sh

set -e

echo "========================================"
echo "  hytf 项目部署开始"
echo "========================================"

# 拉取最新代码
echo "[1/4] 拉取最新代码..."
git pull origin hytf

# 停止旧容器
echo "[2/4] 停止旧容器..."
sudo docker-compose down

# 重新构建并启动
echo "[3/4] 构建并启动容器（首次需要 5-15 分钟）..."
sudo docker-compose up -d --build

# 清理悬空镜像
echo "[4/4] 清理旧镜像..."
sudo docker image prune -f

echo "========================================"
echo "  部署完成！"
echo "========================================"
echo ""
echo "容器状态："
sudo docker-compose ps
echo ""
echo "访问地址："
echo "  前端：http://192.144.238.144"
echo "  后端：http://192.144.238.144:8080"
echo ""
echo "查看日志：sudo docker-compose logs -f"
