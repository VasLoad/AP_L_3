class FileOpenMethods:
    READ = "read"
    WRITE = "write"

class FileError(Exception):
    """Базовые исключения, связанные с файлами."""

    pass


class FileSuffixError(FileError):
    """Ошибка расширения файла."""

    def __init__(self, expected_suffix: str, actual_suffix: str):
        super().__init__(f"Ошибка расширения файла.\nОжидаемое расширение: {expected_suffix}, полученное расширение: {actual_suffix}.")


class FileOpenError(FileError):
    """Ошибка открытия файла."""

    def __init__(self, path: str, error_text: str, method: str):
        if method is FileOpenMethods.READ:
            method_text = "чтении файла"
        elif method is FileOpenMethods.WRITE:
            method_text = "записи в файл"
        else:
            method_text = "работе с файлом"

        super().__init__(f"Ошибка при {method_text} {path}.\nТекст ошибки: {error_text}")


class FileReadError(FileOpenError):
    def __init__(self, path: str, error_text: str):
        super().__init__(path, error_text, FileOpenMethods.READ)


class FileWriteError(FileOpenError):
    def __init__(self, path: str, error_text: str):
        super().__init__(path, error_text, FileOpenMethods.WRITE)
