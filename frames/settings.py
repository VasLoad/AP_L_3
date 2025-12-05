import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Any

from config import SETTINGS_STYLE_PATH, APP_NAME
from enums.route import Route
from enums.theme_mode import ThemeMode
from enums.settings import SettingsParam, Language, Difficulty, Challenges
from frames.base import BaseFrame

from settings import DEFAULT_SETTINGS, MIN_FONT_SIZE, MAX_FONT_SIZE, Settings

from utils.validators import num_validator, enum_value_validator


class SettingsRadioButton(ttk.Radiobutton):
    """Класс кастомизированного элемента ttk.Radiobutton"""

    def __init__(self, *args, **kwargs):
        kwargs["style"] = "SettingsRadioButton.TRadiobutton"

        super().__init__(*args, **kwargs)


class SettingsGroup(ABC, ttk.LabelFrame):
    """Базовый класс для любой группы настроек"""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(master, text=text, style="SettingsLabelFrame.TLabelframe", padding=25, **kwargs)

    @property
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, value):
        pass


class LanguageGroup(SettingsGroup):
    def __init__(self, master, initial_value: Language):
        super().__init__(master, " Язык текста ")
        self.__var = tk.StringVar(value=initial_value)

        for lang in Language:
            SettingsRadioButton(
                self,
                text=lang.label,
                variable=self.__var,
                style="SettingsRadioButton.TRadiobutton",
                value=lang
            ).pack(side="left", padx=(0, 20))

    @property
    def get(self) -> str:
        return self.__var.get()

    def set(self, value: Language):
        if enum_value_validator(value, Language):
            self.__var.set(Language(value))


class DifficultyGroup(SettingsGroup):
    def __init__(self, master, initial_value: Difficulty):
        super().__init__(master, " Сложность ")
        self.__var = tk.StringVar(value=initial_value)

        for difficulty in Difficulty:
            SettingsRadioButton(
                self,
                text=difficulty.label,
                variable=self.__var,
                value=difficulty
            ).pack(side="left", padx=(0, 20))

    @property
    def get(self) -> str:
        return self.__var.get()

    def set(self, value: Difficulty):
        if enum_value_validator(value, Difficulty):
            self.__var.set(Difficulty(value))


class ThemeGroup(SettingsGroup):
    def __init__(self, master, controller, initial_mode: ThemeMode):
        super().__init__(master, " Тема оформления ")
        self.__controller = controller
        self.__var = tk.Variable(value=initial_mode)

        SettingsRadioButton(
            self,
            text="Светлая",
            variable=self.__var,
            value=ThemeMode.LIGHT,
            command=lambda: controller.toggle_theme_mode(ThemeMode.LIGHT)
        ).pack(side="left", padx=(0, 20))

        SettingsRadioButton(
            self,
            text="Тёмная",
            variable=self.__var,
            value=ThemeMode.DARK,
            command=lambda: controller.toggle_theme_mode(ThemeMode.DARK)
        ).pack(side="left")

    @property
    def get(self) -> ThemeMode:
        return ThemeMode(self.__var.get())

    def set(self, value: ThemeMode):
        if enum_value_validator(value, ThemeMode):
            self.__var.set(ThemeMode(value))


class ChallengesGroup(SettingsGroup):
    def __init__(self, master, initial_values: dict):
        super().__init__(master, " Усложнения ")

        self.__on_time_var = tk.BooleanVar()

        self.__unpack_settings(initial_values)

        ttk.Checkbutton(
            self,
            text=Challenges.ON_TIME.label,
            variable=self.__on_time_var,
            style="SettingsCheckbutton.TCheckbutton",
            onvalue=True,
            offvalue=False
        ).pack(side="left", padx=(0, 20))

    @property
    def get(self) -> dict[str, Any]:
        return {
            Challenges.ON_TIME: self.__on_time_var.get()
        }

    def set(self, value: dict):
        self.__unpack_settings(value)

    def __unpack_settings(self, settings: dict):
        self.__on_time_var.set(
            settings.get(
                Challenges.ON_TIME.value,
                DEFAULT_SETTINGS.get(SettingsParam.CHALLENGES.value).get(Challenges.ON_TIME.value)
            )
        )


class FontSizeGroup(SettingsGroup):
    def __init__(self, master, initial_size: int):
        super().__init__(master, " Размер шрифта ")

        self.__var = tk.IntVar()

        self.set(initial_size)

        scale = ttk.Scale(
            self,
            from_=MIN_FONT_SIZE,
            to=MAX_FONT_SIZE,
            orient="horizontal",
            variable=self.__var,
            command=lambda _: self.__on_change()
        )
        scale.pack(fill="x", pady=(5, 10), padx=10)

        # self.__var.trace("w", self.__on_change)

        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(fill="x", pady=(0, 15), padx=10)

        ttk.Label(ctrl_frame, text="Значение:", style="SettingsParamValueLabel.TLabel").pack(side="left")
        entry = ttk.Entry(ctrl_frame, textvariable=self.__var, width=5, justify="center")
        entry.pack(side="left", padx=(5, 0))

        self.preview = ttk.Label(
            self,
            text="Аа Бб Вв - Aa Bb Cc - 12345 !?#@",
            padding=25
        )
        self.preview.pack(fill="x")

        self.__update_preview()

    def __on_change(self):
        self.__update_preview()

    def __update_preview(self):
        size = self.__var.get()

        self.preview.config(font=("Segoe UI", size))

    def __get_validated_value(self) -> int:
        value: int = num_validator(self.__var.get(), MIN_FONT_SIZE, MAX_FONT_SIZE)

        return value

    @property
    def get(self) -> int:
        return self.__get_validated_value()

    def set(self, value: int):
        self.__var.set(num_validator(value, MIN_FONT_SIZE, MAX_FONT_SIZE))


class SettingsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, f"{APP_NAME} - Настройки")

        self.__language_group = None
        self.__difficulty_group = None
        self.__theme_group = None
        self.__challenges_group = None
        self.__font_group = None

    @property
    def content(self) -> ttk.Frame:
        frame = ttk.Frame(self._parent)

        title = ttk.Label(
            frame,
            text="НАСТРОЙКИ",
            style="FrameTitle.TLabel",
        )
        title.pack(pady=(0, 25))

        groups_container = ttk.Frame(frame)
        groups_container.pack(fill="both")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(25, 0))

        ttk.Button(
            btn_frame,
            text="ПРИМЕНИТЬ И ВЕРНУТЬСЯ",
            style="SettingApplyAndBackButton.TButton",
            command=self.__apply_and_back
        ).pack(side="left", padx=15)

        self.__layout_groups(groups_container)

        return frame

    def __layout_groups(self, groups_container: ttk.Frame):
        current: Settings = self._controller.settings

        self.__language_group = LanguageGroup(
            groups_container,
            initial_value=current.language
        )
        self.__difficulty_group = DifficultyGroup(
            groups_container,
            initial_value=current.difficulty
        )
        self.__theme_group = ThemeGroup(
            groups_container,
            controller=self._controller,
            initial_mode=self._controller.theme_mode
        )
        self.__challenges_group = ChallengesGroup(
            groups_container,
            initial_values=current.challenges
        )
        self.__font_group = FontSizeGroup(
            groups_container,
            initial_size=current.font_size
        )

        for group in (self.__language_group, self.__difficulty_group, self.__theme_group, self.__challenges_group, self.__font_group):
            group.pack(fill="x", pady=(0, 5))

    def __apply_and_back(self):
        new_settings = {
            SettingsParam.LANGUAGE.value: self.__language_group.get,
            SettingsParam.DIFFICULTY.value: self.__difficulty_group.get,
            SettingsParam.FONT_SIZE.value: self.__font_group.get,
            SettingsParam.CHALLENGES.value: self.__challenges_group.get,
            SettingsParam.THEME_MODE.value: self.__theme_group.get.value
        }

        self._controller.save_settings(new_settings)

        self._controller.go(Route.ROUTE_BACK)

    def _configure_style(self, style: ttk.Style):
        self._controller.configure_style_by_path(style, SETTINGS_STYLE_PATH)

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
