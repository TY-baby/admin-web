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


# 档位日消耗（用于计算消耗条数）与单条消耗随机区间（不含上界）
TIER_DAILY_BUDGET = {"A": 300, "B": 600, "C": 1000}
TIER_ITEM_RANGE = {"A": (30, 199), "B": (200, 499), "C": (500, 1000)}

NOVEL_TIER_PRICE = {"A": 998, "B": 1998, "C": 3998}
NOVEL_READ_RANGE = {"A": (0, 500), "B": (500, 2000), "C": (2000, 5000)}


def gen_page_code(existing: set) -> str:
    while True:
        code = str(random.randint(10000, 99999))
        if code not in existing:
            return code


def decide_tier(amount: float):
    if amount >= 500:
        return "C", 1000
    if amount >= 200:
        return "B", 600
    return "A", 300
