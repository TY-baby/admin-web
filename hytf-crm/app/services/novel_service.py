import os
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.logging_conf import logger
from app.models.douyin_account import DouyinAccount
from app.models.finance_log import FinanceLog
from app.models.novel_page import NovelPage
from app.utils.id_generator import NOVEL_READ_RANGE, NOVEL_TIER_PRICE, gen_page_code

NOVEL_DIR = os.environ.get("NOVEL_DIR", "/app/novel_book")
GROW_SECONDS = 3600

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>深度布局网文推广赛道，恒耀互娱以“平台+运营”双引擎模式重构创作者价值生态</title>
<style>
body{margin:0;background:#f5f6f8;font-family:"Microsoft YaHei",Arial,sans-serif;color:#333}
.wrap{max-width:860px;margin:0 auto;background:#fff;padding:28px 32px 40px}
h1{font-size:24px;line-height:1.5;margin:8px 0 14px}
.meta{color:#999;font-size:13px;border-bottom:1px solid #eee;padding-bottom:12px;margin-bottom:18px}
.meta span{margin-right:18px}
#reads{color:#e64340;font-weight:bold;font-style:normal}
p{font-size:16px;line-height:1.9;text-indent:2em;margin:14px 0}
.footer{margin-top:28px;border-top:1px solid #eee;padding-top:14px;color:#aaa;font-size:12px;line-height:1.8}
</style>
</head>
<body>
<div class="wrap">
<h1>深度布局网文推广赛道，恒耀互娱以“平台+运营”双引擎模式重构创作者价值生态</h1>
<div class="meta"><span>日期：{date_str}</span><span>编辑：网文频道</span><span>来源：恒耀互娱</span><span>阅读: <em id="reads">0</em></span></div>
<p>近日，网文推广赛道持续升温。恒耀互娱以“平台+运营”双引擎模式，为创作者提供覆盖内容分发、数据追踪与结算服务的全链路推广能力，助力优质内容更精准地触达目标读者。</p>
<p>据平台负责人介绍，投放期间系统将基于实时数据反馈持续优化投放策略，保障推广效果稳定、数据透明可查，并为创作者提供阶段性结算依据。</p>
<p>行业观察人士指出，随着更多创作者与服务商加入，网文推广生态正从粗放买量走向精细化运营，数据可视化与结算效率将成为核心竞争力。</p>
<div class="footer">版权声明：转载此文是出于传递更多信息之目的。若有来源标注错误或侵犯了您的合法权益，请作者与本网联系，我们将及时更正、删除，谢谢您的支持与理解。<br/>广告内容请自行辨别，本站不参与任何推荐与导购。</div>
</div>
<script>
fetch('/api/v1/public/novel/{code}/reads').then(function(r){return r.json();}).then(function(d){if(d&&d.code===0){document.getElementById('reads').innerText=d.data.reads;}}).catch(function(){});
</script>
</body>
</html>
"""


def current_reads(p: NovelPage, now: datetime = None) -> int:
    now = now or datetime.utcnow()
    elapsed = max(0.0, (now - p.created_at).total_seconds())
    start, cap = p.reads_start, p.reads_cap
    if elapsed >= GROW_SECONDS:
        base = cap
    else:
        k = 0.7 + (p.seed % 100) / 100.0 * 0.9
        base = start + int((cap - start) * ((elapsed / GROW_SECONDS) ** k))
    return base + (p.refresh_count or 0)


def page_link(p: NovelPage) -> str:
    return f"http://www.hytf.com.cn/book/{p.page_code}.html"


def _write_file(p: NovelPage):
    os.makedirs(NOVEL_DIR, exist_ok=True)
    html = HTML_TEMPLATE.replace("{code}", p.page_code) \
        .replace("{date_str}", p.created_at.strftime("%Y-%m-%d"))
    path = os.path.join(NOVEL_DIR, f"{p.page_code}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"[novel page generated] {path}")


def launch_novel(db: Session, cid: int, douyin_id: str, tier: str):
    a = db.query(DouyinAccount).filter(DouyinAccount.customer_id == cid,
                                       DouyinAccount.douyin_id == douyin_id).first()
    if not a:
        raise ValueError("douyin account not found")
    price = NOVEL_TIER_PRICE[tier]
    balance = float(a.balance)
    if balance < price:
        raise ValueError("账号余额不足,请联系管理员充值")
    consumed = price * int(balance // price)
    remaining = round(balance - consumed, 2)
    codes = {c for (c,) in db.query(NovelPage.page_code).all()}
    page = NovelPage(customer_id=cid, account_id=a.id, douyin_id=douyin_id,
                     page_code=gen_page_code(codes), tier=tier, unit_price=price,
                     consumed=consumed,
                     reads_start=NOVEL_READ_RANGE[tier][0],
                     reads_cap=NOVEL_READ_RANGE[tier][1],
                     seed=random.randint(1, 1000000), refresh_count=0,
                     created_at=datetime.utcnow())
    db.add(page)
    a.balance = remaining
    db.add(FinanceLog(customer_id=cid, douyin_account_id=a.id, change_type="CONSUME",
                      amount=-consumed, balance_after=remaining,
                      stat_date=datetime.utcnow(), remark="网文一键投放结算"))
    db.commit()
    db.refresh(page)
    _write_file(page)
    return page, consumed, remaining