from datetime import datetime
import re


def to_snake_case(text: str) -> str:
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def format_date(value: datetime):
    return value.strftime("%b %d %Y %H:%M:%S")


def str_is_true(value: str) -> bool:
    if isinstance(value, bool):
        return value
    return value.lower() in ["1", "true", "yes", "y"]


def read_all_content_from_file(file_path, encoding="utf-8") -> str:
    with open(file_path, "r", encoding=encoding) as fp:
        return fp.read()
