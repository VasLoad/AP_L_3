import re
from typing import Optional

from utils.storage import load_txt


def load_text_from_file(path: str) -> str:
    try:
        text = load_txt(path)
    except Exception:
        raise

    return text


def load_text_from_file_with_regex(path: str, regex_pattern: Optional[str] = None) -> list[str]:
    try:
        text = load_txt(path)
    except Exception:
        raise

    return re.findall(re.compile(regex_pattern), text)
