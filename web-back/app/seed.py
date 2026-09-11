import datetime
from .database import SessionLocal
from .models import User, News
from .security import hash_password

SAMPLE_NEWS = [
    {"title": "Base Room 完成 B 轮融资，加速数字化推流布局", "category": "公司新闻",
     "summary": "本轮融资将用于技术研发与市场拓展，进一步巩固行业领先地位。",
     "url": "https://www.base-room.cn/news/1", "fee": 12.50},
    {"title": "2026 智慧园区一体化解决方案正式发布", "category": "产品发布",
     "summary": "全新一体化智慧园区平台，覆盖安防、能源、运营全场景。",
     "url": "https://www.base-room.cn/news/2", "fee": 8.00},
    {"title": "行业峰会：AI 如何赋能企业流量增长", "category": "行业动态",
     "summary": "专家齐聚，共同探讨人工智能在流量运营中的落地实践。",
     "url": "https://www.base-room.cn/news/3", "fee": 15.80},
    {"title": "Base Room 与多家头部企业达成战略合作", "category": "公司新闻",
     "summary": "强强联合，共建数字化生态，实现互利共赢。",
     "url": "https://www.base-room.cn/news/4", "fee": 6.60},
    {"title": "新版数据大屏上线，实时洞察业务全貌", "category": "产品发布",
     "summary": "可视化能力全面升级，支持多维度实时数据监控。",
     "url": "https://www.base-room.cn/news/5", "fee": 9.90},
    {"title": "技术分享：高并发点击追踪系统的设计实践", "category": "技术前沿",
     "summary": "从架构到落地，揭秘稳定高效的埋点统计方案。",
     "url": "https://www.base-room.cn/news/6", "fee": 3.50},
    {"title": "Base Room 荣获年度最佳数字化服务商称号", "category": "行业动态",
     "summary": "权威认可，见证实力，感谢每一位客户的支持。",
     "url": "https://www.base-room.cn/news/7", "fee": 20.00},
    {"title": "招贤纳士：加入我们，共创数字未来", "category": "公司新闻",
     "summary": "多个技术、产品岗位火热招聘中，期待你的加入。",
     "url": "https://www.base-room.cn/news/8", "fee": 1.00},
]


def init_data():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add(User(username="admin", password=hash_password("123456"), real_name="管理员"))
            print("[SEED] admin / 123456 created")

        if db.query(News).count() == 0:
            now = datetime.datetime.now()
            for i, item in enumerate(SAMPLE_NEWS):
                db.add(News(**item, publish_time=now - datetime.timedelta(hours=i * 5)))
            print(f"[SEED] {len(SAMPLE_NEWS)} news inserted")

        db.commit()
    finally:
        db.close()