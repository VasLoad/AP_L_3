from tkinter import ttk

from config import APP_NAME
from enums.route import Route
from frames.base import BaseFrame


class MenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Центральная часть
        center_frame = ttk.Frame(self, style="Main.TFrame")
        center_frame.grid(row=1, column=0, sticky="nsew")
        center_frame.grid_columnconfigure(0, weight=1)

        # ——— Заголовок ———
        title = ttk.Label(
            center_frame,
            text=APP_NAME,
            style="Title.TLabel"
        )
        title.grid(row=0, column=0)

        # Подзаголовок (по желанию)
        subtitle = ttk.Label(
            center_frame,
            text="Клавиатурный тренажёр",
            foreground="#8888bb",
            font=("Segoe UI Light", 20)
        )
        subtitle.grid(row=1, column=0, pady=(0, 50))

        # ——— Кнопки ———
        btn_config = {
            "style": "Menu.TButton",
            "width": 20,
            "cursor": "hand2"
        }

        btn_play = ttk.Button(
            center_frame,
            text="ТРЕНАЖЁР",
            command=lambda: controller.go(Route.ROUTE_GAME),
            **btn_config
        )
        btn_play.grid(row=2, column=0, pady=(0, 25))

        btn_settings = ttk.Button(
            center_frame,
            text="НАСТРОЙКИ",
            command=lambda: controller.go(Route.ROUTE_SETTINGS),
            **btn_config
        )
        btn_settings.grid(row=3, column=0, pady=(0, 25))

        btn_exit = ttk.Button(
            center_frame,
            text="ВЫХОД",
            command=controller.destroy,
            **btn_config
        )
        btn_exit.grid(row=4, column=0)

    @staticmethod
    def _configure_style(style: ttk.Style):
        style.configure(
            "Menu.TButton",
            font=("Segoe UI", 20, "bold"),
            borderwidth=0,
            focuscolor="none",
            padding=(20, 18)
        )

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
