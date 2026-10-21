"""统一时间工具：全系统按北京时间（东八区,24小时制）记录与计算。
不依赖容器 TZ/tzdata，显式偏移，避免 UTC 慢 8 小时问题。"""
from datetime import date, datetime, timedelta, timezone

CN_TZ = timezone(timedelta(hours=8))


def now_cn() -> datetime:
    """当前北京时间（naive, 24小时制）"""
    return datetime.now(CN_TZ).replace(tzinfo=None)


def today_cn() -> date:
    """当前北京日期"""
    return datetime.now(CN_TZ).date()