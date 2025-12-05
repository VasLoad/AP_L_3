import tkinter as tk
from tkinter import messagebox, ttk
import sv_ttk
from functools import cached_property
from typing import Optional, Any

from config import APP_NAME, MAIN_STYLE_PATH, STYLES_DIR_PATH, ROUTE_SPECIAL_SYMBOL
from frames.base import BaseFrame
from settings import SETTINGS_FILE_PATH, DEFAULT_SETTINGS, Settings

from enums.route import Route
from enums.theme_mode import ThemeMode
from enums.settings import SettingsParam

from frames.menu import MenuFrame
from frames.settings import SettingsFrame
from frames.trainer import TrainerFrame

from utils.storage import load_json, save_json, get_files_paths_from_dir_path


class Application(tk.Tk):
    """Главный элемент приложения."""

    def __init__(
            self,
            title: str,
            settings_file_path: str,
            frames: dict,
            theme_mode: ThemeMode = ThemeMode.DARK,
            geometry: Optional[str] = None
    ):
        super().__init__()

        self.__style: ttk.Style
        self.__start_style()

        self._theme_mode = theme_mode
        self.theme_mode = self._theme_mode

        self.title(title)

        if geometry:
            self.geometry(geometry)

        self.__settings_file_path = settings_file_path
        self.__settings: Settings = Settings(DEFAULT_SETTINGS)
        self.load_settings(apply=True)

        self.__container: tk.Frame = self.__build_container()

        self.__frames: dict[Route, type[BaseFrame]] = frames

        self.__frame: Optional[BaseFrame] = None

        self.__content: Optional[ttk.Frame] = None

        self.__route: Optional[Route] = None

        self.__routes_history: list[Route] = []

    @property
    def settings_file_path(self) -> str:
        return self.__settings_file_path

    @property
    def route(self) -> Optional[Route]:
        return self.__route

    @route.setter
    def route(self, value: Route):
        self.go(value)

    def go(self, route: Route, force_refresh: bool = False):
        if not force_refresh and self.__route == route and self.__content:
            self.__frame.refresh(self.__style)

            return

        if route not in self.__frames.keys() and  route.value[0] != ROUTE_SPECIAL_SYMBOL:
            return

        if route is Route.ROUTE_BACK:
            if len(self.__routes_history) > 1:
                self.__routes_history.pop()

                route = self.__routes_history[-1]
        else:
            self.__routes_history.append(route)

        self.__frame = None

        if self.__content:
            self.__content.destroy()

            self.__content = None

        frame_class = self.__frames.get(route)

        if not frame_class:
            return

        frame = frame_class(parent=self.__container, controller=self)

        frame.refresh(self.__style)

        frame_content = frame.content

        frame_content.grid(row=0, column=0, sticky="nsew")

        self.__frame = frame

        self.__content = frame_content

        self.__route = route

    @property
    def theme_mode(self) -> ThemeMode:
        return self._theme_mode

    @theme_mode.setter
    def theme_mode(self, value: Optional[ThemeMode] = None):
        self.toggle_theme_mode(value)

    def toggle_theme_mode(self, theme_mode: Optional[ThemeMode] = None):
        """
        Смена темы приложения.

        Args:
            theme_mode: Тема приложения (опционально)
        """

        new_theme_mode: ThemeMode = theme_mode

        if not new_theme_mode:
            if self._theme_mode is ThemeMode.DARK:
                new_theme_mode = ThemeMode.LIGHT
            else:
                new_theme_mode = ThemeMode.DARK

        try:
            sv_ttk.set_theme(new_theme_mode)
        except Exception as ex:
            self.show_error("Ошибка смены темы", f"Не удалось сменить тему.\nТекст ошибки: {ex}.")

        self.refresh_styles()

        self._theme_mode = new_theme_mode

    @property
    def settings(self) -> Settings:
        self.load_settings()

        return self.__settings

    @settings.setter
    def settings(self, value: Settings):
        if not value:
            self.show_error("Пустой параметр", "Параметр value не может быть пустым!")
        else:
            self.__settings = value

    def load_settings(self, default_data: Optional[dict[str, Any]] = DEFAULT_SETTINGS, path: Optional[str] = SETTINGS_FILE_PATH, apply: bool = False):
        """
        Загрузка настроек из файла .JSON.

        Args:
            default_data: Настройки по умолчанию (опционально)
            path: Путь к файлу настроек (опционально)
            apply: Применить настройки?
        """

        try:
            settings = load_json(path)

            if not settings:
                settings = default_data

                self.save_settings(settings)
        except Exception as ex:
            self.show_warning(
                "Не удалось загрузить настройки",
                f"Текст ошибки:\n{str(ex)}\nБудут загружены настройки по умолчанию."
            )

            settings = default_data

            self.save_settings(settings)

        self.settings = Settings(settings)

        if apply:
            self.apply_settings()

    def apply_settings(self):
        """Применить настройки."""

        try:
            theme_mode = ThemeMode(self.settings.theme_mode)

            self.toggle_theme_mode(theme_mode)
        except ValueError as ex:
            self.show_warning(
                "Неверное значение параметра theme_mode",
                f"Текст ошибки:\n{ex}\nЗначение параметра theme_mode будет установлено по умолчанию"
            )

            self.toggle_theme_mode(DEFAULT_SETTINGS.get(SettingsParam.THEME_MODE.value))

    def save_settings(self, data: dict[str, Any], path: Optional[str] = None):
        """
        Сохранить настройки в файл .JSON.

        Args:
            data: Настройки в формате словаря
            path: Путь к файлу настроек (опционально)
        """

        if not path:
            path = self.__settings_file_path

        try:
            save_json(path, data)
        except Exception as ex:
            self.show_error(
                "Не удалось сохранить настройки",
                f"Текст ошибки:\n{str(ex)}"
            )

    @cached_property
    def default_settings(self) -> dict[str, Any]:
        return DEFAULT_SETTINGS

    @staticmethod
    def show_error(title: str = "Ошибка", message: str = "Произошла неизвестная ошибка"):
        messagebox.showerror(title=title, message=f"{message}")

    @staticmethod
    def show_warning(title: str = "Предупреждение", message: str = ""):
        messagebox.showwarning(title=title, message=message)

    @staticmethod
    def show_info(title: str = "Информация", message: str = ""):
        messagebox.showinfo(title=title, message=message)

    def __start_style(self):
        """Создать исходный стиль."""

        self.__style = ttk.Style()

        self.configure_style_by_path(self.__style, MAIN_STYLE_PATH)

    def refresh_styles(self) -> ttk.Style:
        """Перезагрузить стили."""

        style = self.__style

        paths: list[str] = get_files_paths_from_dir_path(STYLES_DIR_PATH)

        for path in paths:
            self.configure_style_by_path(style, path)

        return style

    def configure_style_by_path(self, style, path):
        """
        Настроить стиль из файла .JSON.

        Args:
            style: Исходный стиль
            path: Путь к файлу стиля
        """

        try:
            styles = load_json(path)
        except Exception as ex:
            self.show_error("Ошибка обновления стилей", f"Произошла ошибка при обновлении стилей.\nТекст ошибка: {ex}.")

            return

        for widget_style, params in styles.items():
            style.configure(
                widget_style,
                **params
            )

    def __build_container(self) -> tk.Frame:
        """Создать контейнер для фреймов."""

        container = tk.Frame(self, padx=25, pady=25)

        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)

        container.grid_columnconfigure(0, weight=1)

        return container


if __name__ == "__main__":
    app = Application(
        APP_NAME,
        SETTINGS_FILE_PATH,
        {
            Route.ROUTE_MENU: MenuFrame,
            Route.ROUTE_TRAINER: TrainerFrame,
            Route.ROUTE_SETTINGS: SettingsFrame
        },
        geometry="1250x950"
    )

    app.go(Route.ROUTE_MENU)

    app.mainloop()
