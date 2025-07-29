import re


def validate_length(value: str, min_value: int, max_value: int) -> bool:
    stripped_ = value.strip()
    return min_value <= len(stripped_) <= max_value


def validate_allowed(postcode: str, pattern: str) -> bool:
    return bool(re.match(pattern, postcode))
