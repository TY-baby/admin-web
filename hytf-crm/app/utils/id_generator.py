import json
import random
import string
from datetime import datetime
from typing import List, Dict, Any

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
# 基础规则：A档300/条→随机(280~290)；B档600/条→随机(480~490)；C档1000/条→随机(980~990)
# gen_launch_items 使用 randint(lo, hi-1)，故上界需 +1 才能取到 290/490/990
TIER_ITEM_RANGE = {"A": (280, 291), "B": (480, 491), "C": (980, 991)}

# 直播曝光度（1h内曝光）：档位价格与曝光量随机区间（不含上界）
EXPOSURE_TIER_PRICE = {"A": 1998, "B": 2998, "C": 5998}
EXPOSURE_TIER_RANGE = {"A": (1000, 3000), "B": (3000, 5000), "C": (5000, 10000)}

NOVEL_TIER_PRICE = EXPOSURE_TIER_PRICE
NOVEL_READ_RANGE = {"A": (1000, 3000), "B": (3000, 5000), "C": (5000, 10000)}

LAUNCH_TYPE_LABEL = {"FIRST_CHARGE": "首充", "EXPOSURE": "直播曝光度"}


def gen_launch_items(count: int, item_range: tuple) -> List[Dict[str, Any]]:
    """一次性生成 count 条 {biz_code, nickname, value}，用于投放时落库"""
    lo, hi = item_range
    items = []
    for _ in range(max(0, count)):
        val = random.randint(lo, hi - 1) if hi > lo else lo
        items.append({
            "biz_code": f"{random.randint(0, 999999):06d}",
            "nickname": gen_nickname(),
            "value": val,
        })
    return items


def dump_items(items: List[Dict[str, Any]]) -> str:
    return json.dumps(items or [], ensure_ascii=False)


def load_item_batches(raw) -> List[Dict[str, Any]]:
    """投放明细按批次解析：[{"launch_at": "YYYY-mm-dd HH:MM:SS"|None, "items": [...]}]
       兼容旧的平铺结构 [{biz_code,...}]，视为单批次且 launch_at=None"""
    if not raw:
        return []
    try:
        v = json.loads(raw)
    except Exception:
        return []
    if not isinstance(v, list) or not v:
        return []
    if isinstance(v[0], dict) and "biz_code" in v[0]:
        return [{"launch_at": None, "items": v}]
    out = []
    for b in v:
        if isinstance(b, dict) and isinstance(b.get("items"), list):
            out.append({"launch_at": b.get("launch_at"), "items": b["items"]})
    return out


def append_launch_batch(raw, items: List[Dict[str, Any]], launch_at: datetime) -> str:
    """本次投放明细追加为新批次（多次投放累加，不覆盖）"""
    batches = load_item_batches(raw)
    batches.append({"launch_at": launch_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "items": items or []})
    return json.dumps(batches, ensure_ascii=False)


def load_items(raw) -> List[Dict[str, Any]]:
    """平铺展开全部批次明细（多次投放累计）"""
    return [it for b in load_item_batches(raw) for it in b["items"]]


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
