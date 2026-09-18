#!/bin/bash
# hytf 一键部署脚本
# 用法: bash deploy.sh
# 说明: 优先使用 Compose V2 (docker compose)，兼容旧版 docker-compose

set -e

# 自动选择 compose 命令：优先 V2 插件版（避免 v1 的 KeyError: 'ContainerConfig' bug）
if sudo docker compose version >/dev/null 2>&1; then
    COMPOSE="sudo docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE="sudo docker-compose"
else
    echo "未检测到 docker compose，请先执行: bash server-setup.sh"
    exit 1
fi
echo "使用 compose 命令: $COMPOSE"

echo "========================================"
echo "  hytf 项目部署开始"
echo "========================================"

# 拉取最新代码
echo "[1/4] 拉取最新代码..."
git pull origin hytf

# 停止旧容器
echo "[2/4] 停止旧容器..."
$COMPOSE down

# 重新构建并启动
echo "[3/4] 构建并启动容器（首次需要 5-15 分钟）..."
$COMPOSE up -d --build

# 清理悬空镜像
echo "[4/4] 清理旧镜像..."
sudo docker image prune -f

echo "========================================"
echo "  部署完成！"
echo "========================================"
echo ""
echo "容器状态："
$COMPOSE ps
echo ""
echo "访问地址："
echo "  前端：http://192.144.238.144"
echo "  后端：http://192.144.238.144:8080"
echo ""
echo "查看日志：$COMPOSE logs -f"
