from datetime import datetime


def normalize_error_detail(detail) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, dict):
        if isinstance(detail.get("detail"), str):
            return detail["detail"]
        if isinstance(detail.get("message"), str):
            return detail["message"]
        return str(detail)
    if isinstance(detail, list):
        messages: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                loc = item.get("loc")
                field = ".".join(str(x) for x in loc[1:]) if isinstance(loc, (list, tuple)) and len(loc) > 1 else "参数"
                msg = item.get("msg")
                if msg:
                    messages.append(f"{field}: {msg}")
            else:
                messages.append(str(item))
        return "；".join(messages) if messages else "请求参数不合法"
    return "请求失败"


def normalize_csv_headers(row: dict) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in row.items():
        if key is None:
            continue
        normalized_key = key.strip().lstrip("\ufeff").lower()
        normalized[normalized_key] = value
    return normalized


def read_csv_value(row: dict[str, str], *keys: str, default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is not None:
            return str(value).strip()
    return default


def parse_csv_date(value: str) -> datetime:
    if not value:
        return datetime.now()
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.now()


def month_range(year: int, month: int) -> tuple[datetime, datetime]:
    start = datetime(year, month, 1, 0, 0, 0, 0)
    if month == 12:
        next_month = datetime(year + 1, 1, 1, 0, 0, 0, 0)
    else:
        next_month = datetime(year, month + 1, 1, 0, 0, 0, 0)
    return start, next_month
