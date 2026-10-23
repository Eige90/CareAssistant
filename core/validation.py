import re
from PySide6.QtCore import QRegularExpression

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

PHONE_ALLOWED_RE = QRegularExpression(r"^\+?[0-9 ()/.-]{0,25}$")


def email_is_valid(text: str) -> bool:
    text = (text or "").strip()
    return not text or bool(EMAIL_RE.fullmatch(text))


def phone_is_valid(text: str) -> bool:
    text = (text or "").strip()
    if not text:
        return True
    digits = re.sub(r"\D", "", text)
    return 5 <= len(digits) <= 15 and bool(re.fullmatch(r"\+?[0-9 ()/.-]+", text))
