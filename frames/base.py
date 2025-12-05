from abc import ABC, abstractmethod
from tkinter import ttk

from config import APP_NAME


class BaseFrame(ABC):
    def __init__(self, parent, controller, title: str = APP_NAME):
        self._parent = parent
        self._controller = controller

        self._controller.title(title)

    @property
    @abstractmethod
    def content(self) -> ttk.Frame:
        pass

    @abstractmethod
    def _configure_style(self, style: ttk.Style):
        pass

    @abstractmethod
    def refresh(self, style: ttk.Style):
        pass
