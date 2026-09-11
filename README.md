# My Project —— 网站推流点击追踪系统

面试演示项目，包含官网、推流管理后台、FastAPI 接口服务三部分。

## 一、目录结构

    my-project/
    ├── docker-compose.yml        # 三服务编排：MySQL + FastAPI + Nginx
    ├── Dockerfile.frontend       # 一个 Nginx 同时构建托管两个前端
    ├── nginx/default.conf        # 单域名多前端路由 + API 反向代理
    ├── deploy.sh                 # 一键部署
    ├── stop-admin-web.sh         # 下线旧的 admin-web 部署，释放 80 端口
    ├── init-git.ps1              # Git 初始化（同仓库，独立分支 my-project）
    ├── web-pc/                   # 官网前端  Vue2 + vue-cli5
    ├── web-front/                # 推流后台  Vue2 + vue-cli5 + Element UI + Vuex
    └── web-back/                 # 后端接口  Python + FastAPI + SQLAlchemy

## 二、技术栈

| 层 | 技术 |
|---|---|
| 官网前端 web-pc | Vue 2.6 + Vue Router 3 + Axios + SCSS |
| 后台前端 web-front | Vue 2.6 + Element UI 2.15 + Vuex 3 + Vue Router 3 |
| 后端 web-back | Python 3.11 + FastAPI + SQLAlchemy 2.0 + PyMySQL + PyJWT |
| 数据库 | MySQL 8.0（库名 my_project） |
| 部署 | Docker Compose + Nginx 反向代理 |

## 三、单域名部署两个前端（重点）

只有一个域名 www.base-room.cn，通过 Nginx 路径分发实现共存：

| 访问地址 | 指向 | 说明 |
|---|---|---|
| www.base-room.cn/ | web-pc 构建产物 | 官网，publicPath = / |
| www.base-room.cn/admin/ | web-front 构建产物 | 后台，publicPath = /admin/，router base = /admin/ |
| www.base-room.cn/api/ | 反代 backend:8000 | FastAPI 接口 |

三个必须对齐的配置，错一个后台就会白屏或刷新 404：

1. web-front/vue.config.js  ->  publicPath: '/admin/'
2. web-front/src/router/index.js  ->  new VueRouter({ base: '/admin/' })
3. nginx/default.conf  ->  location /admin/ { try_files $uri $uri/ /admin/index.html; }

Dockerfile.frontend 中把两个构建产物分别拷到：

    /usr/share/nginx/html          <- web-pc
    /usr/share/nginx/html/admin    <- web-front

## 四、数据库设计

库名 my_project，三张表由 SQLAlchemy 首次启动自动创建。

### news —— 官网新闻/推广链接源
| 字段 | 说明 |
|---|---|
| id | 主键 |
| title | 新闻标题 |
| category | 栏目分类 |
| summary | 摘要 |
| url | 跳转目标链接 |
| fee | 该链接携带的费用字段 |
| publish_time | 发布时间 |

### click_log —— 点击流水（每点一次写一行）
| 字段 | 说明 |
|---|---|
| id | 主键 |
| news_id | 关联新闻 |
| title | 新闻标题（冗余，便于统计） |
| fee | 本次点击对应费用 |
| url | 本次点击的链接 |
| ip | 点击者真实 IP |
| click_time | 点击时间 |

点击次数不单独存字段，由 click_log 记录条数 COUNT 聚合得出。
好处：并发下不会丢计数，且完整保留每一次的时间与 IP 明细，可审计。

### users —— 后台账号
默认账号 admin，密码 123456（PBKDF2-SHA256 加盐哈希存储）。

## 五、接口清单

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| GET | /api/health | 否 | 健康检查 |
| GET | /api/news | 否 | 官网新闻列表 |
| GET | /api/news/{id} | 否 | 新闻详情 |
| POST | /api/click | 否 | 记录点击（标题/费用/IP/时间） |
| POST | /api/auth/login | 否 | 后台登录，返回 JWT |
| GET | /api/auth/info | 是 | 当前登录用户信息 |
| GET | /api/transactions | 是 | 交易信息聚合列表（分页+搜索） |

统一响应体（与前端 request.js 拦截器约定一致）：

    { "code": 0, "message": "ok", "data": {...} }

code 为 0 表示成功，非 0 前端自动弹错误提示。

## 六、真实 IP 是怎么拿到的

Nginx 反代之后，FastAPI 里 request.client.host 拿到的是 Docker 内网 IP（如 172.18.0.2），
不是访客真实公网 IP。所以：

1. nginx/default.conf 的 location /api/ 中必须配置：
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
2. web-back/app/security.py 的 get_client_ip() 按优先级读取：
       X-Forwarded-For 第一段  ->  X-Real-IP  ->  request.client.host

## 七、本地开发

需要本机已装 Node.js、Python 3.11、MySQL 8.0。

### 1. 启动后端

    cd web-back
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    copy .env.example .env      # 本地开发把 DB_HOST 改成 localhost
    uvicorn app.main:app --reload --port 8000

接口文档（FastAPI 自动生成）：http://localhost:8000/docs

### 2. 启动官网

    cd web-pc
    npm install
    npm run serve

访问 http://localhost:8080 ，/api 已代理到 8000。

### 3. 启动后台

    cd web-front
    npm install
    npm run serve

注意：因为 publicPath 是 /admin/，本地访问地址是
http://localhost:8081/admin/  （不是根路径，直接访问 8081 会 404）

## 八、服务器部署

服务器：腾讯云 Lighthouse，IP 124.220.135.116，域名 www.base-room.cn

### 第 1 步：本地推送代码

    cd D:\personal\project\my-project
    powershell -ExecutionPolicy Bypass -File .\init-git.ps1

会推送到 admin-web 同一仓库的 my-project 分支，不影响 main。

### 第 2 步：服务器拉取代码

    ssh root@124.220.135.116
    cd /www
    git clone -b my-project git@github.com:TY-baby/admin-web.git my-project

### 第 3 步：下线旧的 admin-web 部署（释放 80 端口）

    cd /www/my-project
    chmod +x stop-admin-web.sh deploy.sh
    ./stop-admin-web.sh

### 第 4 步：部署 my-project

    ./deploy.sh

首次构建需拉取 mysql/node/python/nginx 镜像，约 5-15 分钟。

### 第 5 步：放行防火墙端口

腾讯云控制台 -> 实例 -> 防火墙，放行 TCP 80、8000。

### 第 6 步：验证

| 验证项 | 地址 | 预期 |
|---|---|---|
| 官网 | http://www.base-room.cn/ | 显示首页与新闻推送条 |
| 后台 | http://www.base-room.cn/admin/ | 显示科技感登录页 |
| 接口 | http://www.base-room.cn/api/health | {"status":"ok"} |
| 登录 | admin / 123456 | 进入交易信息页 |

演示流程：先在官网点几条新闻（会新开窗口），再登录后台刷新交易信息，
即可看到点击次数、点击时间、IP、费用的实时统计。

## 九、日常更新发版

本地：

    git add -A
    git commit -m "feat: 描述本次修改"
    git push origin my-project

服务器：

    cd /www/my-project
    git pull origin my-project
    ./deploy.sh

只更新单个服务：

    docker-compose up -d --build backend     # 只重建后端
    docker-compose up -d --build frontend    # 只重建前端

## 十、常用运维命令

    docker-compose ps                          # 查看容器状态
    docker-compose logs -f backend             # 跟踪后端日志
    docker logs my-project-backend --tail=50   # 看最近 50 行
    docker exec -it my-project-db mysql -u my_user -pmy_pass_2026 my_project
    docker image prune -f                      # 清理悬空镜像

进数据库后常用查询：

    SELECT COUNT(*) FROM click_log;
    SELECT title, COUNT(*) c FROM click_log GROUP BY title ORDER BY c DESC;
    SELECT * FROM click_log ORDER BY click_time DESC LIMIT 20;

## 十一、故障排查

### 后台 /admin/ 白屏
检查 web-front 的 publicPath 是否为 '/admin/'，且已重新 build。
浏览器 F12 看静态资源请求路径是否带 /admin/ 前缀。

### 后台刷新页面 404
nginx 的 location /admin/ 缺少 try_files 回退到 /admin/index.html。

### 交易信息里 IP 是 172.x 内网地址
nginx 的 /api/ 没有配 proxy_set_header X-Forwarded-For，补上后重建 frontend。

### 点击次数一直是 0
1. 浏览器 F12 -> Network 看 POST /api/click 是否 200
2. docker logs my-project-backend 看有无 [CLICK] 日志
3. 进数据库 SELECT COUNT(*) FROM click_log 确认是否落库

### 后端启动报数据库连接失败
docker-compose ps 看 db 是否 healthy。后端有 20 次 x 3 秒的重试等待，
一般会自动恢复；仍失败则检查 .env / compose 里的 DB_HOST 是否为 db。

### 80 端口被占用，frontend 起不来
说明 admin-web 还没下线，执行 ./stop-admin-web.sh。