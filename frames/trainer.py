import tkinter as tk
from tkinter import ttk

from config import APP_NAME, MENU_STYLE_PATH
from enums.settings import Difficulty
from frames.base import BaseFrame
from enums.route import Route
from settings import Settings


class TrainerFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, f"{APP_NAME} - Тренажёр")

        self.__settings: Settings = self._controller.settings

        self.__difficulty = None

        self.__timer_label = None

        self.__upload_text_btn = None

    @property
    def content(self) -> ttk.Frame:
        frame = ttk.Frame(self._parent)

        font_size = self.__settings.font_size

        header = ttk.Frame(frame, height=50)
        header.pack(fill="x")

        self.__timer_label = ttk.Label(header, text="00:00", font=("Segue UI", 25))
        self.__timer_label.pack_forget()

        header_buttons = ttk.Frame(header)
        header_buttons.pack(side="right", padx=20)

        ttk.Button(header_buttons, text="В меню", width=12, command=lambda: self._controller.go(Route.ROUTE_MENU), style="TrainerHeader.TButton").pack(side="left", padx=5)
        ttk.Button(header_buttons, text="Настройки", width=12, command=lambda: self._controller.go(Route.ROUTE_SETTINGS), style="TrainerHeader.TButton").pack(side="left", padx=5)

        self.__upload_text_btn = ttk.Button(header_buttons, text="Загрузить текст", width=16, style="TrainerHeader.TButton")
        self.__upload_text_btn.pack_forget()

        text_display = tk.Text(
            frame,
            font=("Segoe UI", font_size),
            bg=self._parent.cget("bg"),
            borderwidth=0,
            height=1,
            wrap="word",
            bd=0,
            highlightthickness=0
        )
        text_display.pack(pady=(0, 25), fill="x", expand=True)
        text_display.insert("1.0", "Текст, который будет отображаться...")
        text_display.tag_add("center", "1.0", "end")
        text_display.tag_configure("center", justify="center")
        text_display.config(state="disabled")

        text_input_field = tk.Entry(frame, font=("Segoe UI", font_size), width=50)
        text_input_field.pack()
        text_input_field.bind("<KeyRelease>", None)

        self.__prepare_ui()

        return frame

    def __prepare_ui(self):
        self.__prepare_timer_label()
        self.__prepare_upload_text_button()

    def __prepare_timer_label(self):
        if self.__settings.on_time:
            self.__timer_label.pack(side="left", padx=(0, 25))

    def __prepare_upload_text_button(self):
        if self.__settings.difficulty in [Difficulty.EASY, Difficulty.NORMAL]:
            self.__upload_text_btn.pack(side="left", padx=5)

    def _configure_style(self, style: ttk.Style):
        self._controller.configure_style_by_path(style, MENU_STYLE_PATH)

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
