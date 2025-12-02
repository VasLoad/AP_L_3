from abc import ABC, abstractmethod
from tkinter import ttk

class BaseFrame(ABC, ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    @staticmethod
    @abstractmethod
    def _configure_style(style: ttk.Style):
        pass

    @abstractmethod
    def refresh(self, style: ttk.Style):
        self._configure_style(style)
