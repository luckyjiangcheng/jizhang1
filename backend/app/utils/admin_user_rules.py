import re


PHONE_PATTERN = re.compile(r"^1\d{10}$")


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_PATTERN.match(phone))


def build_initial_password(phone: str) -> str:
    if not is_valid_phone(phone):
        raise ValueError("invalid phone")
    return phone[-6:]
