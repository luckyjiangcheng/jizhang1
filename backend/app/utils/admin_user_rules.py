def is_valid_phone(phone: str) -> bool:
    # 支持数字、中文、英文组合，长度100个字符以内
    return bool(phone and len(phone) <= 100)


def build_initial_password(phone: str) -> str:
    if not is_valid_phone(phone):
        raise ValueError("invalid phone")
    # 对于非数字账号，使用固定密码
    return "123456"
