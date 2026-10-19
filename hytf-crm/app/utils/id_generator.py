import json
import random
import string
from datetime import datetime
from typing import List, Dict, Any

_NICK_P = ["恒", "耀", "星", "辰", "鑫", "盛", "腾", "飞", "达", "汇", "聚", "创", "赢", "锋", "智"]
_NICK_S = ["投手", "推广", "运营", "小助手", "工作站", "达人", "联盟", "旗舰", "先锋", "战队"]

_NICK_CN_CHARS = list(
    "恒耀星辰鑫盛腾飞达汇聚创赢锋智嘉瑞祥福禄寿喜财运气风华正茂青春梦想"
    "龙腾虎跃鹏程万里前程似锦金榜题名步步高升天天开心快乐幸福安康平安如意"
    "吉祥锦绣辉煌璀璨锐意进取开拓创新勇往直前志存高远厚德载物自强不息"
)

PLATFORM_ID_LEN = {
    "liujianfang": (3, 10),
    "bilibili": (8, 10),
    "kuaishou": (9, 11),
    "yingke": (8, 10),
    "qiyin": (7, 9),
}
_DEFAULT_ID_LEN = (6, 10)


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


def gen_platform_id(platform_code: str, existing: set = None) -> str:
    existing = existing if existing is not None else set()
    lo, hi = PLATFORM_ID_LEN.get(platform_code, _DEFAULT_ID_LEN)
    length = random.randint(lo, hi)
    for _ in range(300):
        pid = "".join(random.choices(string.digits, k=length))
        if pid[0] == "0":
            pid = str(random.randint(1, 9)) + pid[1:]
        if pid not in existing:
            existing.add(pid)
            return pid
    pid = "".join(random.choices(string.digits, k=length))
    existing.add(pid)
    return pid


def gen_platform_nickname(existing: set = None) -> str:
    existing = existing if existing is not None else set()
    nick = ""
    for _ in range(300):
        total = random.randint(5, 10)
        mode = random.choice(["cn", "cn_num", "cn_en"])
        if mode == "cn":
            cn_len, extra = total, ""
        elif mode == "cn_num":
            cn_len = random.randint(2, max(2, total - 1))
            extra = "".join(random.choices(string.digits, k=total - cn_len))
        else:
            cn_len = random.randint(2, max(2, total - 1))
            extra = "".join(random.choices(string.ascii_letters, k=total - cn_len))
        nick = "".join(random.choices(_NICK_CN_CHARS, k=cn_len)) + extra
        if nick not in existing:
            existing.add(nick)
            return nick
    existing.add(nick)
    return nick


TIER_DAILY_BUDGET = {"A": 300, "B": 600, "C": 1000}
TIER_ITEM_RANGE = {"A": (280, 291), "B": (580, 591), "C": (980, 991)}

EXPOSURE_TIER_PRICE = {"A": 2998, "B": 3998, "C": 6998}
EXPOSURE_TIER_RANGE = {"A": (800, 1001), "B": (1200, 1501), "C": (2300, 2801)}

NOVEL_TIER_PRICE = EXPOSURE_TIER_PRICE
NOVEL_READ_RANGE = EXPOSURE_TIER_RANGE

LAUNCH_TYPE_LABEL = {"FIRST_CHARGE": "首充", "EXPOSURE": "直播曝光度"}


def gen_recharge_order_no() -> str:
    """充值订单号：年月日 + 随机 8 位纯数字，例：2029080613145201"""
    return datetime.now().strftime("%Y%m%d") + "".join(random.choices(string.digits, k=8))


def gen_launch_items(count: int, item_range: tuple, platform_code: str = "") -> List[Dict[str, Any]]:
    lo, hi = item_range
    items = []
    used_ids: set = set()
    used_nicks: set = set()
    for _ in range(max(0, count)):
        val = random.randint(lo, hi - 1) if hi > lo else lo
        biz_code = gen_platform_id(platform_code, used_ids) if platform_code \
            else f"{random.randint(0, 999999):06d}"
        nickname = gen_platform_nickname(used_nicks)
        items.append({"biz_code": biz_code, "nickname": nickname, "value": val})
    return items


def dump_items(items: List[Dict[str, Any]]) -> str:
    return json.dumps(items or [], ensure_ascii=False)


def load_item_batches(raw) -> List[Dict[str, Any]]:
    if not raw:
        return []
    try:
        v = json.loads(raw)
    except Exception:
        return []
    if not isinstance(v, list) or not v:
        return []
    if isinstance(v[0], dict) and "biz_code" in v[0]:
        return [{"launch_at": None, "tier": None, "launch_type": None,
                 "consumed": None, "items": v}]
    out = []
    for b in v:
        if isinstance(b, dict) and isinstance(b.get("items"), list):
            out.append({
                "launch_at": b.get("launch_at"),
                "tier": b.get("tier"),
                "launch_type": b.get("launch_type"),
                "consumed": b.get("consumed"),
                "items": b["items"],
            })
    return out


def append_launch_batch(raw, items: List[Dict[str, Any]], launch_at: datetime,
                        tier: str = None, launch_type: str = None,
                        consumed: float = None) -> str:
    batches = load_item_batches(raw)
    batches.append({
        "launch_at": launch_at.strftime("%Y-%m-%d %H:%M:%S"),
        "tier": tier,
        "launch_type": launch_type,
        "consumed": consumed,
        "items": items or [],
    })
    return json.dumps(batches, ensure_ascii=False)


def load_items(raw) -> List[Dict[str, Any]]:
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
