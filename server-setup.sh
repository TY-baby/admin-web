#!/bin/bash
# hytf 全新服务器环境初始化脚本（Ubuntu 20.04/22.04）
# 作用：安装 Docker + 配置国内镜像加速 + 安装 docker-compose
# 用法：git clone 项目后，在项目根目录执行  bash server-setup.sh
# 说明：本脚本只做“环境准备”，容器构建启动请用 deploy.sh

set -e

echo "========================================"
echo "  [1/4] 更新 apt 并安装基础工具"
echo "========================================"
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release git

echo "========================================"
echo "  [2/4] 安装 Docker（阿里云镜像源）"
echo "========================================"
if command -v docker >/dev/null 2>&1; then
    echo "Docker 已安装，跳过：$(docker --version)"
else
    curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
fi
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker "$USER"

echo "========================================"
echo "  [3/4] 配置 Docker 国内镜像加速"
echo "========================================"
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json >/dev/null <<-'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "========================================"
echo "  [4/4] 安装 docker-compose"
echo "========================================"
if command -v docker-compose >/dev/null 2>&1; then
    echo "docker-compose 已安装，跳过：$(docker-compose --version)"
else
    sudo apt install -y docker-compose
fi

echo ""
echo "========================================"
echo "  环境初始化完成！版本信息："
echo "========================================"
sudo docker --version
sudo docker-compose --version
echo ""
echo "镜像加速验证："
sudo docker info | grep -A 3 "Registry Mirrors" || true
echo ""
echo ">>> 注意：usermod 加入 docker 组需重新登录 SSH 才免 sudo 生效。"
echo ">>> 下一步执行部署：  bash deploy.sh"
