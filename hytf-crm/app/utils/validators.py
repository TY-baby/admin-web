import re
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")


def is_phone(v: str) -> bool:
    return bool(v and PHONE_RE.match(v))