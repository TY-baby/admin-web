import random
import string
from datetime import datetime

_NICK_P = ["恒", "耀", "星", "辰", "鑫", "盛", "腾", "飞", "达", "汇", "聚", "创", "赢", "锋", "智"]
_NICK_S = ["投手", "推广", "运营", "小助手", "工作站", "达人", "联盟", "旗舰", "先锋", "战队"]


def gen_customer_uid(existing=None) -> str:
    existing = existing or set()
    d = datetime.now().strftime("%Y%m%d")
    for _ in range(200):
        uid = d + f"{random.randint(0, 99):02d}"
        if uid not in existing:
            return uid
    return d + f"{datetime.now().microsecond % 100:02d}"


def gen_auto_code(existing=None) -> str:
    existing = existing or set()
    for _ in range(500):
        c = "".join(random.choices(string.digits, k=6))
        if c not in existing:
            return c
    raise RuntimeError("cannot generate unique 6-digit code")


def gen_nickname(max_len: int = 20) -> str:
    tail = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3, 8)))
    return f"{random.choice(_NICK_P)}{random.choice(_NICK_S)}_{tail}"[:max_len]


def decide_tier(amount: float):
    if amount >= 500:
        return "C", 1000
    if amount >= 200:
        return "B", 600
    return "A", 300
