# hytf-web 鍓嶇

Vue 2.7 + Element UI + Axios + ECharts + Vuex + Vue Router

涓€涓」鐩悓鏃舵壙杞?A绔?瀹㈡埛) 鍜?B绔?绠＄悊鍛? 涓ゅ绯荤粺锛岄€氳繃璺敱鍓嶇紑鍖哄垎銆?

## 蹇€熷惎鍔?

    cd hytf-web
    npm install --registry=https://registry.npmmirror.com
    npm run serve

榛樿璁块棶:
- A绔櫥褰? http://localhost:8081/#/client/login
- B绔櫥褰? http://localhost:8081/#/admin/login  (admin / admin123)

## 鐢熶骇鏋勫缓

    npm run build

鐢熸垚 dist/ 鐩綍锛岄厤鍚?Nginx 鍙嶄唬 /api/* 鍒板悗绔?8080 绔彛鍗冲彲涓婄嚎銆?

## 鐩綍缁撴瀯

    hytf-web/
      public/index.html          HTML 妯℃澘(宸茬鐢ㄥ彸閿?閫夋嫨)
      src/
        main.js                  鍏ュ彛
        App.vue                  鏍圭粍浠?
        permission.js            璺敱瀹堝崼+NProgress
        router/index.js          璺敱琛?A绔?B绔?
        store/
          index.js
          modules/clientUser.js  A绔櫥褰曟€?鎶栭煶鍙峰垪琛?
          modules/adminUser.js   B绔櫥褰曟€?
        api/
          request.js             axios 灏佽(鑷姩闄凾oken,缁熶竴鍝嶅簲)
          clientAuth.js          A绔櫥褰?
          clientHome.js          A绔椤垫暟鎹?
          adminAuth.js           B绔櫥褰?
          adminCustomer.js       B绔鎴风鐞?
          adminInvoice.js        B绔紑绁ㄧ鐞?
          adminDashboard.js      B绔椤电粺璁?
        utils/
          auth.js                Cookie Token 绠＄悊
          validate.js            鎵嬫満鍙?閲戦鏍￠獙
          security.js            闃睩12/闃茶皟璇?闃瞚frame
        styles/index.scss        鍏ㄥ眬鏍峰紡
        components/LineChart.vue 閫氱敤 ECharts 鎶樼嚎鍥?
        layout/AdminLayout.vue   B绔乏渚ц彍鍗曞竷灞€
        views/
          client/                A绔〉闈?
            Login.vue
            Home.vue
            Launch.vue
            Finance.vue
          admin/                 B绔〉闈?
            Login.vue
            Dashboard.vue
            customer/Index.vue
            customer/EditDialog.vue
            invoice/Index.vue

## 鐜鍙橀噺
- .env.development: VUE_APP_API_BASE=http://127.0.0.1:8080
- .env.production:  VUE_APP_API_BASE=(绌?璧?Nginx 鍙嶄唬)
- VUE_APP_ENABLE_SECURITY=true 寮€鍚墠绔槻鎶?

## 瀹夊叏璇存槑
src/utils/security.js 鎻愪緵 F12 鎷︽埅銆佸彸閿鐢ㄣ€丏evTools 妫€娴嬨€侀槻 iframe 宓屽叆绛夈€?
鎵€鏈夊墠绔槻鎶ら兘鍙缁曡繃,浠呮彁楂橀棬妲涖€傛牳蹇冨畨鍏ㄤ緷璧栧悗绔?JWT + 闄愭祦 + 鏉冮檺鏍￠獙銆?