import json
from pathlib import Path
from typing import Any, Optional

from config import DEFAULT_JSON_INDENT
from errors import FileReadError, FileWriteError, FileSuffixError


def get_files_paths_from_dir_path(dir_path: str) -> list[str]:
    """
    Возвращает список путей к файлам, находящихся по переданному пути к директории.

    Args:
        dir_path: Путь к директории для получения списка путей к находящимся в ней файлов

    Returns:
        Список путей к файлам, находящихся по переданному пути к директории
    """

    dir_path = Path(dir_path)

    if not dir_path.exists():
        return []

    files_paths: list[str] = []

    for file_path in dir_path.iterdir():
        if file_path.is_file():
            files_paths.append(str(file_path))

    return files_paths


def merge_dicts(source: dict, update: dict) -> Optional[dict]:
    """
    Совмещает словари.

    Args:
        source: Основной словарь
        update: Словарь с данными для обновления

    Returns:
        Совмещённый словарь (опционально)
    """

    for key, value in update.items():
        if isinstance(value, dict) and key in source and isinstance(source[key], dict):
            merge_dicts(source[key], value)
        else:
            source[key] = value


def load_json(path: str, default_data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """
    Загружает данные из файла .JSON.
    Если данных нет, то возвращает данные по умолчанию (опционально).

    Args:
        path: Путь к файлу данных
        default_data: Данные по умолчанию (опционально)

    Returns:
        Загруженные данные

    Raises:
        FileSuffixError: Неверное расширение файла данных
        FileReadError: Ошибка при чтении файла данных
    """

    path = Path(path)

    if default_data is None:
        default_data = {}

    file_suffix = path.suffix.lower()
    suffix = ".json"

    if file_suffix != suffix:
        raise FileSuffixError(suffix, file_suffix)

    if not path.exists():
        return default_data.copy()

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read().strip()

            if not data:
                return default_data.copy()

            return json.loads(data)
    except (json.JSONDecodeError, PermissionError) as ex:
        raise FileReadError(str(path.absolute()), ex)


def save_json(path: str, data: dict[str, Any], indent: int = DEFAULT_JSON_INDENT):
    """
    Сохраняет данные в файл .JSON, не трогая другие данные.

    Args:
        path: Путь к файлу данных
        data: Данные для сохранения
        indent: Глубина отступов файла .JSON

    Raises:
        FileSuffixError: Неверное расширение файла данных
        FileWriteError: Ошибка при записи в файл данных
    """

    try:
        current_data = load_json(path, default_data={})
    except FileSuffixError:
        raise
    except FileReadError:
        current_data = {}

    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    merge_dicts(current_data, data)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(current_data, f, ensure_ascii=False, indent=indent)
    except (PermissionError, OSError) as ex:
        raise FileWriteError(str(path.absolute()), ex)
