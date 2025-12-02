import tkinter as tk
from tkinter import messagebox, ttk
import sv_ttk
from functools import cached_property
from typing import Optional, Any

from config import APP_NAME, MAIN_TFRAME_STYLE_NAME
from frames.base import BaseFrame
from settings import SETTINGS_FILE_PATH, DEFAULT_SETTINGS

from enums.route import Route
from enums.theme_mode import ThemeMode
from enums.settings import SettingsParam

from frames.menu import MenuFrame
from frames.settings import SettingsFrame
from frames.game import GameFrame

from utils.storage import load_json, save_json


class Application(tk.Tk):
    def __init__(
            self,
            name: str,
            settings_file_path: str,
            frames: dict[Route, BaseFrame],
            theme_mode: ThemeMode = ThemeMode.DARK,
            geometry: Optional[str] = None
    ):
        super().__init__()

        self._theme_mode = theme_mode
        self.theme_mode = self._theme_mode

        self.__name = name

        if geometry:
            self.geometry(geometry)

        self.__settings_file_path = settings_file_path
        self.__settings: dict[str, Any] = {}
        self.load_settings(apply=True)

        self.__configure_style()

        self.__container: tk.Frame = self.__build_container()

        self.__frames: dict[Route, BaseFrame] = self.__build_frames(frames)

        self.__route: Optional[Route] = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def settings_file_path(self) -> str:
        return self.__settings_file_path

    @property
    def route(self) -> Optional[Route]:
        return self.__route

    @route.setter
    def route(self, value: Route):
        self.go(value)

    def go(self, route: Route):
        frame: Optional[BaseFrame] = self.__frames.get(route)

        if not frame:
            return

        self.__route = route

        frame.refresh(self.__configure_style())

        frame.tkraise()

    @property
    def theme_mode(self) -> ThemeMode:
        return self._theme_mode

    @theme_mode.setter
    def theme_mode(self, value: Optional[ThemeMode] = None):
        self.toggle_theme_mode(value)

    def toggle_theme_mode(self, theme_mode: Optional[ThemeMode] = None):
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

        self.__configure_style()

        self._theme_mode = new_theme_mode

    @property
    def settings(self) -> dict[str, Any]:
        return self.__settings.copy()

    @settings.setter
    def settings(self, value: dict[str, Any]):
        if not value:
            self.show_error("Пустой параметр", "Параметр value не может быть пустым!")
        else:
            self.__settings = value.copy()

    def load_settings(self, default_data: Optional[dict[str, Any]] = None, path: Optional[str] = None, apply: bool = False):
        if not path:
            path = self.__settings_file_path

        if not default_data:
            default_data = self.default_settings

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

        self.settings = settings

        if apply:
            self.apply_settings()

    def apply_settings(self):
        try:
            theme_mode = ThemeMode(self.settings.get(SettingsParam.THEME_MODE.value))

            self.toggle_theme_mode(theme_mode)
        except ValueError as ex:
            self.show_warning(
                "Неверное значение параметра theme_mode",
                f"Текст ошибки:\n{ex}\nЗначение параметра theme_mode будет установлено по умолчанию"
            )

            self.toggle_theme_mode(DEFAULT_SETTINGS.get(SettingsParam.THEME_MODE.value))

    def save_settings(self, data: dict[str, Any], path: Optional[str] = None):
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

    @property
    def frames(self) -> dict[Route, BaseFrame]:
        return self.__frames.copy()

    @staticmethod
    def show_error(title: str = "Ошибка", message: str = "Произошла неизвестная ошибка"):
        messagebox.showerror(title=title, message=f"{message}")

    @staticmethod
    def show_warning(title: str = "Предупреждение", message: str = ""):
        messagebox.showwarning(title=title, message=message)

    @staticmethod
    def show_info(title: str = "Информация", message: str = ""):
        messagebox.showinfo(title=title, message=message)

    @staticmethod
    def __configure_style() -> ttk.Style:
        style = ttk.Style()

        style.configure(MAIN_TFRAME_STYLE_NAME)

        style.configure(
            "Title.TLabel",
            font=(
                "Russo One",
                45,
                "bold"
            )
        )

        return style

    def __build_container(self) -> tk.Frame:
        container = tk.Frame(self, padx=25, pady=25)

        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)

        container.grid_columnconfigure(0, weight=1)

        return container

    def __build_frames(self, raw_frames: dict) -> dict[Route, BaseFrame]:
        frames = {}

        for route, frame_class in raw_frames.items():
            frame = frame_class(parent=self.__container, controller=self)

            frame.configure(style=MAIN_TFRAME_STYLE_NAME)

            frame.grid(row=0, column=0, sticky="nsew")

            frames[route] = frame

        return frames


if __name__ == "__main__":
    app = Application(
        APP_NAME,
        SETTINGS_FILE_PATH,
        {
            Route.ROUTE_MENU: MenuFrame,
            Route.ROUTE_GAME: GameFrame,
            Route.ROUTE_SETTINGS: SettingsFrame
        }
    )

    app.go(Route.ROUTE_MENU)

    app.mainloop()
