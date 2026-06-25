# Base Room 腾讯云 Lighthouse 部署指南

本文档记录如何将 base-room 项目部署到腾讯云 Lighthouse（轻量应用服务器）Ubuntu 系统。

## 环境信息

- 服务器：腾讯云 Lighthouse
- 实例名称：penclaw-3xpe
- 系统：Ubuntu 22.04（推荐）
- 项目本地路径：`D:\personal\project\base-room`
- 服务器部署路径：`/www/base-room`
- 默认账号：`admin`
- 默认密码：`123456`

---

## 一、连接服务器

### 1.1 获取公网 IP

登录 [腾讯云 Lighthouse 控制台](https://console.cloud.tencent.com/lighthouse/instance/index)，找到实例，复制公网 IP。

### 1.2 通过 SSH 连接

在本地 PowerShell 中执行：

```powershell
ssh root@你的公网IP
# 或者如果是 ubuntu 用户
ssh ubuntu@你的公网IP
```

也可以直接在 Lighthouse 控制台点击「登录」，通过浏览器终端连接。

---

## 二、安装 Docker

由于国内网络原因，安装 Docker 官方脚本可能会超时，建议使用阿里云镜像源。

### 2.1 使用阿里云脚本安装

```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

如果失败，使用手动安装：

```bash
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 2.2 启动 Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 2.3 配置国内镜像加速

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
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
```

验证镜像源：

```bash
docker info | grep -A 5 "Registry Mirrors"
```

---

## 三、安装 Docker Compose

由于 GitHub 访问不稳定，建议通过 apt 安装：

```bash
sudo apt update
sudo apt install -y docker-compose
docker-compose --version
```

---

## 四、上传项目代码

### 方式 A：通过 scp 上传（推荐首次使用）

在本地 PowerShell 中执行：

```powershell
scp -r D:\personal\project\base-room ubuntu@你的公网IP:/www/
```

### 方式 B：通过 Git 拉取

如果项目已推送到 GitHub：

```bash
cd /www
git clone https://github.com/你的用户名/base-room.git
```

---

## 五、配置环境变量

```bash
cd /www/base-room/base-back
cp .env.example .env
```

编辑 `.env`：

```bash
nano .env
```

写入以下内容：

```env
PORT=3000
JWT_SECRET=base-room-secret-key-2026
JWT_EXPIRES_IN=24h

DB_HOST=mysql
DB_PORT=3306
DB_USER=base_user
DB_PASSWORD=base_pass_2026
DB_NAME=base_room
```

> **注意**：`DB_HOST` 必须填 `mysql`，因为 `docker-compose.yml` 中数据库服务名为 `mysql`。

---

## 六、启动项目

```bash
cd /www/base-room
chmod +x deploy.sh
./deploy.sh
```

首次构建会拉取 MySQL、Node、Nginx 镜像，可能需要 5-15 分钟。

### 查看启动日志

```bash
cd /www/base-room
docker-compose logs -f
```

当看到后端输出 `Server running on http://localhost:3000` 时表示启动成功。

---

## 七、放行防火墙端口

进入腾讯云 Lighthouse 控制台 → 实例详情 → 防火墙 → 添加规则：

| 协议 | 端口 | 策略 |
|------|------|------|
| TCP | 80 | 允许 |
| TCP | 443 | 允许 |
| TCP | 3000 | 允许（测试用） |

---

## 八、访问系统

浏览器打开：

```
http://你的公网IP
```

- 账号：`admin`
- 密码：`123456`

测试后端接口：

```
http://你的公网IP:3000/api/dashboard/stats
```

---

## 九、常见问题

### 9.1 Docker 拉取镜像超时

确保已配置国内镜像源，并重启 Docker：

```bash
sudo systemctl restart docker
```

### 9.2 Python-dotenv 解析 .env 失败

通常是 Windows 换行符或 BOM 导致，重新生成 .env：

```bash
cd /www/base-room/base-back
rm -f .env
cat > .env << 'EOF'
PORT=3000
JWT_SECRET=base-room-secret-key-2026
JWT_EXPIRES_IN=24h

DB_HOST=mysql
DB_PORT=3306
DB_USER=base_user
DB_PASSWORD=base_pass_2026
DB_NAME=base_room
EOF
```

### 9.3 docker-compose 文件不存在

如果 `chmod +x /usr/local/bin/docker-compose` 报错，说明下载失败，改用 apt 安装：

```bash
sudo apt install -y docker-compose
```

### 9.4 页面能打开但接口不通

检查 Nginx 反向代理配置，或前端 `request.js` 中的 `baseURL` 是否保持为 `/api`。

---

## 十、后续更新代码

### 手动更新

```bash
cd /www/base-room
git pull origin main
./deploy.sh
```

### 自动更新（GitHub Actions）

已配置 `.github/workflows/deploy.yml`，只需在 GitHub 仓库 Secrets 中设置：

| Secret 名称 | 说明 |
|------------|------|
| TENCENT_HOST | 服务器公网 IP |
| TENCENT_USER | 服务器用户名 |
| TENCENT_SSH_KEY | 服务器私钥 |

每次推送代码到 `main` 分支会自动触发部署。

---

## 附录：项目结构

```
base-room/
├── docker-compose.yml          # Docker 编排
├── deploy.sh                   # 部署脚本
├── base-front/                 # Vue2 PC 管理系统 + 智慧大屏
├── base-back/                  # Node + Express + MySQL 后端
└── base-app/                   # uni-app 移动端
```
