# hytf-web 前端

Vue 2.7 + Element UI + Axios + ECharts + Vuex + Vue Router

一个项目同时承载 A端(客户) 和 B端(管理员) 两套系统，通过路由前缀区分。

## 快速启动

    cd hytf-web
    npm install --registry=https://registry.npmmirror.com
    npm run serve

默认访问:
- A端登录: http://localhost:8081/#/client/login
- B端登录: http://localhost:8081/#/admin/login  (admin / admin123)

## 生产构建

    npm run build

生成 dist/ 目录，配置 Nginx 反代 /api/* 到后端 8080 端口即可上线。

## 目录结构

    hytf-web/
      public/index.html          HTML 模板(已禁用右键 选择)
      src/
        main.js                  入口
        App.vue                  根组件
        permission.js            路由守卫+NProgress
        router/index.js          路由表 A端 B端
        store/
          index.js
          modules/clientUser.js  A端登录态 抖音号列表
          modules/adminUser.js   B端登录态
        api/
          request.js             axios 封装(自动附Token,统一响应)
          clientAuth.js          A端登录
          clientHome.js          A端首页数据
          adminAuth.js           B端登录
          adminCustomer.js       B端客户管理
          adminInvoice.js        B端开票管理
          adminDashboard.js      B端首页统计
        utils/
          auth.js                Cookie Token 管理
          validate.js            手机号 金额校验
          security.js            防F12/防调试/防iframe
        styles/index.scss        全局样式
        components/LineChart.vue 通用 ECharts 折线图
        layout/AdminLayout.vue   B端左侧菜单布局
        views/
          client/                A端页面
            Login.vue
            Home.vue
            Launch.vue
            Finance.vue
          admin/                 B端页面
            Login.vue
            Dashboard.vue
            customer/Index.vue
            customer/EditDialog.vue
            invoice/Index.vue

## 环境变量
- .env.development: VUE_APP_API_BASE=http://127.0.0.1:8080
- .env.production:  VUE_APP_API_BASE=(空, 走 Nginx 反代)
- VUE_APP_ENABLE_SECURITY=true 开启前端防护

## 安全说明
src/utils/security.js 提供 F12 拦截、右键禁用、DevTools 检测、防 iframe 嵌入等。
所有前端防护都可被绕过,仅提高门槛。核心安全依赖后端 JWT + 限流 + 权限校验。
