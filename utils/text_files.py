import re
from typing import Optional

from errors import FileSuffixError, FileReadError

from utils.storage import load_txt


def load_text_from_file_with_regex(path: str, regex_pattern: Optional[str] = None) -> list[str]:
    """
    Получает данные из файла прогоняет их через регулярное выражение.

    Args:
        path: Путь к файлу
        regex_pattern: Паттерн регулярного выражения (опционально)

    Raises:
        FileSuffixError: Неверное расширение файла данных
        FileReadError: Ошибка при чтении файла данных
    """
    try:
        text = load_txt(path)
    except FileSuffixError:
        raise
    except FileReadError:
        raise

    return re.findall(re.compile(regex_pattern), text)
