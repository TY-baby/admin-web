# hytf-crm 后端

FastAPI + MySQL + Redis，为 A端(客户) 和 B端(管理员) 提供统一 REST API。

## 快速启动

    cd hytf-crm
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS hytf_crm DEFAULT CHARSET utf8mb4;"
    python run.py

访问 http://localhost:8080/docs 查看 Swagger 接口文档。

## 默认账号
- B端管理员: admin / admin123 (首次启动自动创建，请尽快修改)
- A端客户: B端录入手机号后自动生成，密码 = 手机号 + 123

## 目录结构

    hytf-crm/
      app/
        core/          配置/日志/安全/依赖注入
        db/            SQLAlchemy + Redis
        models/        5 张表 ORM
        schemas/       Pydantic 请求响应模型
        services/      业务逻辑
        api/v1/        路由 client_* / admin_*
        middlewares/   安全头 + 限流
        utils/         ID生成 / 校验 / Excel导出
        main.py        FastAPI 入口
      sql/init.sql     生产环境建表脚本
      .env             环境变量
      requirements.txt 依赖清单
      run.py           开发启动入口

## 服务器预警 (2核8G)
- CPU > 80% / 内存 > 80% / QPS > 200 时后端日志 WARN
- 通过 .env 的 ALERT_* 调整阈值
- GET /health 返回实时资源占用

## 安全策略
- JWT 双通道 (A端 12h / B端 2h)
- 登录接口限流 5次/分钟, 普通接口 120次/分钟
- 安全响应头 X-Frame-Options / X-Content-Type-Options / XSS-Protection
- 密码 bcrypt 哈希存储
- 手机号 / 抖音ID 正则 + 长度校验

## 主要接口
- POST /api/v1/client/auth/login       A端登录
- GET  /api/v1/client/home/accounts    A端抖音号下拉
- GET  /api/v1/client/home/summary     A端资金总览
- GET  /api/v1/client/home/trend       A端折线图数据
- POST /api/v1/admin/auth/login        B端登录
- GET  /api/v1/admin/customer/list     客户列表
- POST /api/v1/admin/customer/create   新建客户
- GET  /api/v1/admin/customer/export   导出 Excel
- GET  /api/v1/admin/dashboard/overview B端首页统计
- GET  /api/v1/admin/invoice/list      开票列表
- POST /api/v1/admin/invoice/{id}/process 标记已开票
