import hashlib
import secrets
from datetime import datetime


def generate_license_code(seed: str | None = None) -> str:
    base = seed or secrets.token_urlsafe(16)
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest().upper()
    return f"LC-{digest[:12]}"


def normalize_license_status(status: str | object) -> str:
    if hasattr(status, "value"):
        return str(getattr(status, "value"))
    return str(status)


def is_installable_status(status: str | object) -> bool:
    return normalize_license_status(status) == "unused"


def is_callable_status(status: str | object) -> bool:
    return normalize_license_status(status) == "used"


def now_utc() -> datetime:
    return datetime.utcnow()
