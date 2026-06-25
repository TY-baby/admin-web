# Base Room 开发到发布完整流程

> 本文档记录从本地代码修改到服务器发布的完整操作流程，供后续开发维护参考。

---

## 一、技术架构概览

```
┌─────────────┐    Git Push     ┌──────────┐    Git Pull     ┌──────────────────┐
│  本地开发    │ ──────────────→ │ GitHub   │ ──────────────→ │ 腾讯云服务器      │
│  (Windows)  │   SSH 协议      │  仓库    │   SSH 协议      │ 124.220.135.116  │
└─────────────┘                 └──────────┘                 └──────────────────┘
                                                                      │
                                                              Docker Compose
                                                                      │
                                            ┌─────────────────────────┼─────────────────────────┐
                                            │                         │                         │
                                      ┌─────┴─────┐          ┌───────┴───────┐         ┌──────┴──────┐
                                      │  MySQL 8.0 │          │  Node.js 18   │         │ Nginx Alpine│
                                      │  (数据库)   │          │  (后端 :3000)  │         │ (前端 :80)   │
                                      └───────────┘          └───────────────┘         └─────────────┘
```

### 项目结构

```
admin-web/
├── base-front/          # Vue2 前端（PC管理后台 + 智慧大屏）
│   ├── src/views/       # 页面组件
│   ├── src/api/         # API 请求
│   ├── Dockerfile       # 前端构建镜像（node → nginx）
│   └── nginx.conf       # Nginx 反向代理配置
├── base-back/           # Node.js + Express 后端
│   ├── controllers/     # 业务控制器
│   ├── models/          # 数据库模型 + init.sql
│   ├── routes/          # API 路由
│   ├── app.js           # 入口文件
│   └── Dockerfile       # 后端运行镜像
├── base-app/            # uni-app 移动端（独立项目）
├── docker-compose.yml   # 三服务编排（MySQL + Backend + Frontend）
├── deploy.sh            # 一键部署脚本
├── deploy-guide.md      # 首次部署指南
└── dev-workflow.md      # 本文档（开发发布流程）
```

### 关键配置

| 配置项 | 值 | 位置 |
|--------|-----|------|
| 服务器 IP | 124.220.135.116 | 腾讯云 Lighthouse |
| 服务器项目目录 | /www/base-room | 服务器 |
| Git 仓库 | git@github.com:TY-baby/admin-web.git | SSH 协议 |
| 分支 | main | 唯一发布分支 |
| 前端端口 | 80 | Nginx |
| 后端端口 | 3000 | Express |
| MySQL 端口 | 3306 | 内部/外部 |
| 默认账号 | admin / 123456 | init.sql 初始化 |

---

## 二、本地开发

### 2.1 项目本地路径

```
D:\personal\project\admin-web
```

### 2.2 前端开发（base-front）

```powershell
cd D:\personal\project\admin-web\base-front
npm install          # 首次安装依赖
npm run serve        # 启动开发服务器 (http://localhost:8080)
```

- 开发模式下 API 自动代理到 `http://localhost:3000`（vue.config.js 中配置）
- 页面文件在 `src/views/` 下按模块分目录
- 路由配置在 `src/router/index.js`

### 2.3 后端开发（base-back）

```powershell
cd D:\personal\project\admin-web\base-back
npm install          # 首次安装依赖
node app.js          # 启动后端 (http://localhost:3000)
```

- 需要本地 MySQL 运行，或连接远程 MySQL
- 本地开发时在 `base-back/.env` 中配置数据库连接（`DB_HOST=localhost`）
- 数据库初始化脚本在 `models/init.sql`，启动时自动执行

### 2.4 修改代码注意事项

| 修改内容 | 影响范围 | 需要重建 |
|----------|---------|---------|
| `base-front/src/` 下的 Vue 文件 | 前端 | frontend 容器 |
| `base-front/nginx.conf` | Nginx 配置 | frontend 容器 |
| `base-front/Dockerfile` | 前端构建流程 | frontend 容器 |
| `base-back/controllers/` | API 逻辑 | backend 容器 |
| `base-back/models/` | 数据库结构 | backend + mysql 容器 |
| `base-back/app.js` | 服务入口 | backend 容器 |
| `base-back/config/` | 后端配置 | backend 容器 |
| `docker-compose.yml` | 服务编排 | 全部容器 |

---

## 三、Git 提交与推送

### 3.1 Git 配置

本项目使用 **SSH 协议**推送（因为 HTTPS 443 端口被封锁）：

```
remote: git@github.com:TY-baby/admin-web.git
```

本地 Git 已配置 SSH 密钥连接 GitHub。

### 3.2 提交流程

在 PowerShell 中执行（注意：PowerShell 不支持 `&&`，用 `;` 分隔命令）：

```powershell
# 1. 进入项目目录
cd D:\personal\project\admin-web

# 2. 查看修改了哪些文件
git status

# 3. 暂存所有修改
git add -A

# 4. 提交（写清楚本次修改内容）
git commit -m "fix: 简要描述本次修改"

# 5. 推送到 GitHub
git push origin main
```

### 3.3 Commit 信息规范

建议使用以下前缀：

| 前缀 | 含义 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: 新增客户导入功能` |
| `fix:` | 修复 Bug | `fix: 修复502错误和大屏图表` |
| `style:` | 样式/UI 调整 | `style: 优化工作台卡片布局` |
| `refactor:` | 代码重构 | `refactor: 重构数据库连接池` |
| `docs:` | 文档更新 | `docs: 更新部署流程文档` |
| `chore:` | 配置/构建 | `chore: 更新 docker-compose 配置` |

---

## 四、服务器发布

### 4.1 连接服务器

```powershell
# 方式一：SSH 命令行
ssh root@124.220.135.116

# 方式二：腾讯云控制台 → 实例 → 登录（浏览器终端）
```

### 4.2 拉取最新代码

```bash
cd /www/base-room
git pull origin main
```

### 4.3 重新部署

根据修改范围选择部署方式：

#### 方式一：常规更新（推荐，适用于大多数场景）

```bash
cd /www/base-room
sudo docker-compose down
sudo docker-compose up -d --build
```

- `down` 停止所有容器（保留数据卷）
- `up -d --build` 重新构建镜像并后台启动
- **数据库数据不会丢失**

#### 方式二：仅更新前端

```bash
cd /www/base-room
sudo docker-compose up -d --build frontend
```

#### 方式三：仅更新后端

```bash
cd /www/base-room
sudo docker-compose up -d --build backend
```

#### 方式四：完全重建（慎用，会清除数据库）

```bash
cd /www/base-room
sudo docker-compose down -v        # -v 删除数据卷（清除所有数据）
sudo docker-compose up -d --build  # 重新构建，init.sql 重新初始化
```

> **⚠️ 警告**：`down -v` 会删除 MySQL 中所有数据！仅在需要重置数据时使用。

### 4.4 一键部署脚本

```bash
cd /www/base-room
chmod +x deploy.sh
./deploy.sh
```

`deploy.sh` 会自动执行 `down → up -d --build → 清理旧镜像`。

---

## 五、部署后验证

### 5.1 检查容器状态

```bash
sudo docker-compose ps
```

正常输出（三个容器都是 `Up` 状态）：

```
NAME                    STATUS
base-room-mysql         Up (healthy)
base-room-backend       Up
base-room-frontend      Up
```

### 5.2 检查后端健康

```bash
# 健康检查接口（无需登录）
curl http://localhost:3000/api/health
# 预期返回: {"status":"ok","uptime":...}
```

### 5.3 查看后端日志

```bash
sudo docker logs base-room-backend --tail=30
```

正常日志应包含：

```
[APP] Server running on http://localhost:3000
[DB] Database ensured: base_room
[DB] Running 20 CREATE statements...
[DB] Users count: 3 (already seeded)
[DB] Initialization complete
[APP] Database initialization completed successfully
```

### 5.4 查看前端日志

```bash
sudo docker logs base-room-frontend --tail=10
```

### 5.5 浏览器验证

| 验证项 | 地址 | 预期 |
|--------|------|------|
| 前端首页 | http://124.220.135.116 | 显示登录页 |
| 后端健康 | http://124.220.135.116/api/health | `{"status":"ok"}` |
| 登录测试 | 账号 admin / 密码 123456 | 登录成功进入工作台 |
| 智慧大屏 | http://124.220.135.116/bigscreen | 图表正常渲染 |
| API 数据 | 登录后访问各列表页 | 数据正常加载 |

---

## 六、常用运维命令

### 6.1 容器管理

```bash
# 查看运行中的容器
sudo docker-compose ps

# 重启某个服务
sudo docker-compose restart backend
sudo docker-compose restart frontend

# 停止所有服务
sudo docker-compose stop

# 启动已停止的服务
sudo docker-compose start
```

### 6.2 日志查看

```bash
# 查看所有服务日志（实时跟踪）
sudo docker-compose logs -f

# 只看后端日志
sudo docker logs -f base-room-backend

# 只看最近 50 行
sudo docker logs base-room-backend --tail=50
```

### 6.3 数据库操作

```bash
# 进入 MySQL 命令行
sudo docker exec -it base-room-mysql mysql -u base_user -pbase_pass_2026 base_room

# 常用 SQL
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM customers;
SELECT * FROM users WHERE username = 'admin';
```

### 6.4 清理空间

```bash
# 清理悬空镜像
sudo docker image prune -f

# 清理所有未使用的镜像和容器
sudo docker system prune -f

# 查看磁盘使用
sudo docker system df
```

---

## 七、完整操作示例（日常发版）

以下是一次典型的代码修改到发布的全过程：

### Step 1：本地修改代码

```powershell
# 在本地用 IDE 修改代码
# 例如：修改了 base-front/src/views/customer/index.vue
```

### Step 2：本地测试

```powershell
cd D:\personal\project\admin-web\base-front
npm run serve
# 浏览器打开 http://localhost:8080 验证修改效果
```

### Step 3：提交推送

```powershell
cd D:\personal\project\admin-web
git add -A
git commit -m "feat: 客户列表新增批量删除功能"
git push origin main
```

### Step 4：服务器拉取部署

```bash
# SSH 连接服务器
ssh root@124.220.135.116

# 拉取代码
cd /www/base-room
git pull origin main

# 重新部署
sudo docker-compose down
sudo docker-compose up -d --build
```

### Step 5：验证

```bash
# 检查容器状态
sudo docker-compose ps

# 检查后端
curl http://localhost:3000/api/health
```

然后浏览器打开 http://124.220.135.116 验证功能。

---

## 八、故障排查

### 8.1 502 Bad Gateway

**原因**：后端容器未正常运行

```bash
# 查看后端状态
sudo docker-compose ps | grep backend

# 查看后端日志
sudo docker logs base-room-backend --tail=30

# 重启后端
sudo docker-compose restart backend
```

### 8.2 页面显示乱码

**原因**：编码问题

```bash
# 确认 Nginx charset 配置
sudo docker exec base-room-frontend cat /etc/nginx/conf.d/default.conf | head -5

# 重建前端
sudo docker-compose up -d --build frontend
```

### 8.3 数据库连接失败

```bash
# 检查 MySQL 状态
sudo docker-compose ps | grep mysql

# 查看 MySQL 日志
sudo docker logs base-room-mysql --tail=20

# 尝试手动连接
sudo docker exec -it base-room-backend node -e "require('./models/db').query('SELECT 1').then(r => console.log(r)).catch(e => console.error(e.message))"
```

### 8.4 推送代码失败（SSH 连接超时）

```powershell
# 检查 SSH 连接
ssh -T git@github.com

# 如果超时，检查代理配置
# Git 使用 SSH 协议（非 HTTPS），需要 SSH 密钥已添加到 GitHub
```

### 8.5 构建时间过长

Docker 构建会拉取基础镜像和安装 npm 依赖，首次构建可能需要 5-15 分钟。后续构建会使用缓存，通常 1-3 分钟。

```bash
# 查看构建进度
sudo docker-compose up -d --build

# 如果卡在 npm install，可能是网络问题，重启重试即可
```

---

## 九、快速参考卡片

```
┌──────────────────────────────────────────────────────────────┐
│                    日常发版速查                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  本地：                                                      │
│    git add -A                                                │
│    git commit -m "描述"                                       │
│    git push origin main                                      │
│                                                              │
│  服务器：                                                     │
│    ssh root@124.220.135.116                                  │
│    cd /www/base-room                                         │
│    git pull origin main                                      │
│    sudo docker-compose down                                  │
│    sudo docker-compose up -d --build                         │
│                                                              │
│  验证：                                                      │
│    sudo docker-compose ps          # 容器状态                 │
│    curl localhost:3000/api/health  # 后端健康                 │
│    浏览器 http://124.220.135.116   # 前端页面                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
