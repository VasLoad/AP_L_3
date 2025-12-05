from tkinter import ttk

from config import APP_NAME, MENU_STYLE_PATH
from enums.route import Route
from frames.base import BaseFrame


class MenuFrame(BaseFrame):
    """Главное меню."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller, f"{APP_NAME} - Меню")

    @property
    def content(self) -> ttk.Frame:
        frame = ttk.Frame(self._parent)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=2)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        center_frame = ttk.Frame(frame) # style="Main.TFrame"
        center_frame.grid(row=1, column=0, sticky="nsew")
        center_frame.grid_columnconfigure(0, weight=1)

        title = ttk.Label(
            center_frame,
            text=APP_NAME,
            style="Title.TLabel"
        )
        title.grid(row=0, column=0)

        subtitle = ttk.Label(
            center_frame,
            text="Клавиатурный тренажёр",
            font=("Segoe UI Light", 20)
        )
        subtitle.grid(row=1, column=0, pady=(0, 50))

        btn_play = ttk.Button(
            center_frame,
            text="ТРЕНАЖЁР",
            command=lambda: self._controller.go(Route.ROUTE_TRAINER),
            style="Menu.TButton"
        )
        btn_play.grid(row=2, column=0, pady=(0, 25))

        btn_settings = ttk.Button(
            center_frame,
            text="НАСТРОЙКИ",
            command=lambda: self._controller.go(Route.ROUTE_SETTINGS),
            style="Menu.TButton"
        )
        btn_settings.grid(row=3, column=0, pady=(0, 25))

        btn_exit = ttk.Button(
            center_frame,
            text="ВЫХОД",
            command=self._controller.destroy,
            style="Menu.TButton"
        )
        btn_exit.grid(row=4, column=0)

        return frame

    def _configure_style(self, style: ttk.Style):
        self._controller.configure_style_by_path(style, MENU_STYLE_PATH)

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
