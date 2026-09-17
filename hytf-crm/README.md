# hytf-crm 鍚庣

FastAPI + MySQL + Redis锛屼负 A绔?瀹㈡埛) 鍜?B绔?绠＄悊鍛? 鎻愪緵缁熶竴 REST API銆?

## 蹇€熷惎鍔?

    cd hytf-crm
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS hytf_crm DEFAULT CHARSET utf8mb4;"
    python run.py

璁块棶 http://localhost:8080/docs 鏌ョ湅 Swagger 鎺ュ彛鏂囨。銆?

## 榛樿璐﹀彿
- B绔鐞嗗憳: admin / admin123 (棣栨鍚姩鑷姩鍒涘缓锛岃灏藉揩淇敼)
- A绔鎴? B绔綍鍏ユ墜鏈哄彿鍚庤嚜鍔ㄧ敓鎴愶紝瀵嗙爜 = 鎵嬫満鍙?+ 123

## 鐩綍缁撴瀯

    hytf-crm/
      app/
        core/          閰嶇疆/鏃ュ織/瀹夊叏/渚濊禆娉ㄥ叆
        db/            SQLAlchemy + Redis
        models/        5 寮犺〃 ORM
        schemas/       Pydantic 璇锋眰鍝嶅簲妯″瀷
        services/      涓氬姟閫昏緫
        api/v1/        璺敱 client_* / admin_*
        middlewares/   瀹夊叏澶?+ 闄愭祦
        utils/         ID鐢熸垚 / 鏍￠獙 / Excel瀵煎嚭
        main.py        FastAPI 鍏ュ彛
      sql/init.sql     鐢熶骇鐜寤鸿〃鑴氭湰
      .env             鐜鍙橀噺
      requirements.txt 渚濊禆娓呭崟
      run.py           寮€鍙戝惎鍔ㄥ叆鍙?

## 鏈嶅姟鍣ㄩ璀?(2鏍?G)
- CPU > 80% / 鍐呭瓨 > 80% / QPS > 200 鏃跺悗绔棩蹇?WARN
- 閫氳繃 .env 涓?ALERT_* 璋冩暣闃堝€?
- GET /health 杩斿洖瀹炴椂璧勬簮鍗犵敤

## 瀹夊叏绛栫暐
- JWT 鍙岄€氶亾 (A绔?12h / B绔?2h)
- 鐧诲綍鎺ュ彛闄愭祦 5娆?鍒嗛挓, 鏅€氭帴鍙?120娆?鍒嗛挓
- 瀹夊叏鍝嶅簲澶?X-Frame-Options / X-Content-Type-Options / XSS-Protection
- 瀵嗙爜 bcrypt 鍝堝笇瀛樺偍
- 鎵嬫満鍙?/ 鎶栭煶ID 姝ｅ垯 + 闀垮害鏍￠獙

## 涓昏鎺ュ彛
- POST /api/v1/client/auth/login       A绔櫥褰?
- GET  /api/v1/client/home/accounts    A绔姈闊冲彿涓嬫媺
- GET  /api/v1/client/home/summary     A绔祫閲戞€昏
- GET  /api/v1/client/home/trend       A绔姌绾垮浘鏁版嵁
- POST /api/v1/admin/auth/login        B绔櫥褰?
- GET  /api/v1/admin/customer/list     瀹㈡埛鍒楄〃
- POST /api/v1/admin/customer/create   鏂板缓瀹㈡埛
- GET  /api/v1/admin/customer/export   瀵煎嚭 Excel
- GET  /api/v1/admin/dashboard/overview B绔椤电粺璁?
- GET  /api/v1/admin/invoice/list      寮€绁ㄥ垪琛?
- POST /api/v1/admin/invoice/{id}/process 鏍囪宸插紑绁?