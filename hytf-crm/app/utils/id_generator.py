import random
import string
from datetime import datetime

_NICK_P = ["鏄?, "鑰€", "鎭?, "閿?, "婢?, "鐨?, "娌?, "鍗?, "鍖?, "宸?, "宀?, "浜?, "椋?, "娴?, "鍏?]
_NICK_S = ["鎶曟墜", "鎺ㄥ箍", "杩愯惀", "灏忓姪鎵?, "宸ヤ綔瀹?, "杈句汉", "鑱旂洘", "鏃楄埌", "鍏堥攱", "鎴橀槦"]


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