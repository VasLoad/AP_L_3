import tkinter as tk
from tkinter import ttk
from typing import Any

from enums.route import Route
from enums.theme_mode import ThemeMode
from enums.settings import SettingsParam, Language, Difficulty, Challenges
from frames.base import BaseFrame

from settings import DEFAULT_SETTINGS


class SettingsGroup(ttk.LabelFrame):
    """Базовый класс для любой группы настроек"""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(master, text=text, padding=25, **kwargs)


class LanguageGroup(SettingsGroup):
    def __init__(self, master, initial_value: str = "Русский"):
        super().__init__(master, " Язык текста ")
        self.__var = tk.StringVar(value=initial_value)

        for lang in [Language.RUSSIAN, Language.ENGLISH, Language.MIX]:
            ttk.Radiobutton(
                self,
                text=lang.label,
                variable=self.__var,
                value=lang
            ).pack(side="left", padx=20)

    def get(self) -> str:
        return self.__var.get()


class DifficultyGroup(SettingsGroup):
    def __init__(self, master, initial_value: str = "Обычная"):
        super().__init__(master, " Сложность ")
        self.__var = tk.StringVar(value=initial_value)

        for difficulty in [Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD, Difficulty.INSANE]:
            ttk.Radiobutton(
                self,
                text=difficulty.label,
                variable=self.__var,
                value=difficulty
            ).pack(side="left", padx=20)

    def get(self) -> str:
        return self.__var.get()


class ThemeGroup(SettingsGroup):
    def __init__(self, master, controller, initial_mode: ThemeMode):
        super().__init__(master, " Тема оформления ")
        self.__controller = controller
        self.__var = tk.Variable(value=initial_mode)

        ttk.Radiobutton(
            self,
            text="Светлая",
            variable=self.__var,
            value=ThemeMode.LIGHT,
            command=lambda: controller.toggle_theme_mode(ThemeMode.LIGHT)
        ).pack(side="left", padx=25)

        ttk.Radiobutton(
            self,
            text="Тёмная",
            variable=self.__var,
            value=ThemeMode.DARK,
            command=lambda: controller.toggle_theme_mode(ThemeMode.DARK)
        ).pack(side="left", padx=25)

    def get(self) -> ThemeMode:
        return ThemeMode(self.__var.get())


class ChallengesGroup(SettingsGroup):
    def __init__(self, master, time_initial_value: bool = False):
        super().__init__(master, " Усложнения ")
        self.__on_time_var = tk.BooleanVar(value=time_initial_value)

        ttk.Checkbutton(
            self,
            text=Challenges.ON_TIME.label,
            variable=self.__on_time_var,
            onvalue=True,
            offvalue=False
        ).pack(side="left", padx=20, pady=5)

    def get(self) -> dict[str, Any]:
        return {
            Challenges.ON_TIME: self.__on_time_var.get()
        }


class FontSizeGroup(SettingsGroup):
    def __init__(self, master, initial_size: int = 14):
        super().__init__(master, " Размер шрифта ")
        self.var = tk.IntVar(value=initial_size)

        scale = ttk.Scale(
            self,
            from_=12,
            to=34,
            orient="horizontal",
            variable=self.var,
            command=self.__on_change
        )
        scale.pack(fill="x", pady=(5, 10), padx=10)

        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(fill="x", pady=(0, 15), padx=10)

        ttk.Label(ctrl_frame, text="Значение:").pack(side="left")
        entry = ttk.Entry(ctrl_frame, textvariable=self.var, width=5, justify="center")
        entry.pack(side="left", padx=(5, 0))

        self.preview = ttk.Label(
            self,
            text="Аа Бб Вв Гг — Aa Bb Cc — 12345 !?#@",
            padding=20
        )
        self.preview.pack(fill="x")
        self.__update_preview()

    def __on_change(self, val=None):
        self.__update_preview()

    def __update_preview(self):
        size = self.var.get()

        self.preview.config(font=("Segoe UI", size))

    def __get_validated_value(self) -> int:
        value: int = self.var.get()

        if value < 12:
            value = 12
        if value > 34:
            value = 34

        return value

    def get(self) -> int:
        return self.__get_validated_value()


class SettingsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.__build()
        self.__layout_groups()

    def __build(self):
        title = ttk.Label(
            self,
            text="НАСТРОЙКИ",
            font=("Helvetica", 18, "bold")
        )
        title.pack(pady=(0, 25))

        self.groups_container = ttk.Frame(self)
        self.groups_container.pack(fill="both")

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(25, 0))

        ttk.Button(
            btn_frame,
            text="ПРИМЕНИТЬ И ВЕРНУТЬСЯ",
            style="Accent.TButton",
            command=self.__apply_and_back
        ).pack(side="left", padx=15)

        # ttk.Button(
        #     btn_frame,
        #     text="НАЗАД",
        #     command=lambda: self.controller.go(Route.ROUTE_MENU)
        # ).pack(side="left", padx=15)

    def __layout_groups(self):
        # Создаём группы с текущими значениями из контроллера
        current = self.controller.settings  # предполагаем, что у контроллера есть .settings dict

        self.lang_group = LanguageGroup(
            self.groups_container,
            initial_value=current.get(SettingsParam.LANGUAGE.value, DEFAULT_SETTINGS.get(SettingsParam.LANGUAGE.value))
        )
        self.diff_group = DifficultyGroup(
            self.groups_container,
            initial_value=current.get(SettingsParam.DIFFICULTY.value, DEFAULT_SETTINGS.get(SettingsParam.DIFFICULTY.value))
        )
        self.theme_group = ThemeGroup(
            self.groups_container,
            controller=self.controller,
            initial_mode=self.controller.theme_mode
        )
        self.challenges_group = ChallengesGroup(
            self.groups_container,
            time_initial_value=True
        )
        self.font_group = FontSizeGroup(
            self.groups_container,
            initial_size=current.get(SettingsParam.FONT_SIZE.value, DEFAULT_SETTINGS.get(SettingsParam.FONT_SIZE.value))
        )

        for group in (self.lang_group, self.diff_group, self.theme_group, self.challenges_group, self.font_group):
            group.pack(fill="x", pady=(0, 5))

    def __apply_and_back(self):
        new_settings = {
            SettingsParam.LANGUAGE.value: self.lang_group.get(),
            SettingsParam.DIFFICULTY.value: self.diff_group.get(),
            SettingsParam.FONT_SIZE.value: self.font_group.get(),
            SettingsParam.CHALLENGES.value: self.challenges_group.get(),
            SettingsParam.THEME_MODE.value: self.theme_group.get().value
        }

        self.controller.save_settings(new_settings)
        self.controller.go(Route.ROUTE_MENU)

    @staticmethod
    def _configure_style(style: ttk.Style):
        pass

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
