import tkinter as tk
from tkinter import ttk
import time
import random

from enums.route import Route
from frames.base import BaseFrame


class GameFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.start_time = None
        self.timer_job = None

        # === Основные переменные для статистики ===
        self.correct_chars = 0
        self.total_chars_typed = 0

        # === Заготовленные тексты (можно расширить) ===
        self.texts = [
            "Быстрая бурая лиса прыгает через ленивую собаку.",
            "Программист пишет код быстрее, чем говорит.",
            "В мире много клавиатур, но пальцы всегда найдут дорогу домой.",
            "Тренируй пальцы — и ты станешь мастером набора вслепую.",
            "Скорость мысли ограничена только скоростью твоих рук."
        ]

        # === Верхняя панель: таймер и статистика ===
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=20, fill="x")

        self.timer_label = ttk.Label(top_frame, text="01:00", font=("Helvetica", 36, "bold"))
        self.timer_label.pack(side="left", padx=50)

        self.speed_label = ttk.Label(top_frame, text="0 зн/мин", font=("Helvetica", 24))
        self.speed_label.pack(side="right", padx=50)

        # === Текст для набора ===
        text_frame = ttk.Frame(self)
        text_frame.pack(pady=30)

        self.sample_text = tk.StringVar()
        self.sample_label = ttk.Label(
            text_frame,
            textvariable=self.sample_text,
            font=("Consolas", 20),
            foreground="#555555",
            wraplength=800,
            justify="center"
        )
        self.sample_label.pack()

        # === Поле ввода ===
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=20)

        self.entry = tk.Text(
            input_frame,
            height=5,
            width=80,
            font=("Consolas", 20),
            wrap="word",
            undo=True
        )
        self.entry.pack()

        # Подсвечиваем правильные/неправильные символы
        self.entry.tag_config("correct", background="#c8e6c9")
        self.entry.tag_config("error", background="#ffcdd2")

        # === Нижняя панель кнопок ===
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=30)

        ttk.Button(
            button_frame,
            text="НАЧАТЬ ЗАНОВО",
            command=self.start_training
        ).pack(side="left", padx=20)

        ttk.Button(
            button_frame,
            text="В МЕНЮ",
            command=lambda: controller.go(Route.ROUTE_MENU)  # или Route.ROUTE_MENU
        ).pack(side="right", padx=20)

        # === Привязка событий ===
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<FocusIn>", lambda e: self.entry.config(insertbackground="white"))

        # Запускаем первое задание
        self.start_training()

    def start_training(self):
        """Сброс и запуск нового раунда"""
        # Сбрасываем всё
        self.entry.delete("1.0", "end")
        self.entry.config(state="normal")
        self.entry.focus_set()

        self.correct_chars = 0
        self.total_chars_typed = 0
        self.speed_label.config(text="0 зн/мин")

        # Выбираем случайный текст
        self.current_text = random.choice(self.texts)
        self.sample_text.set(self.current_text)

        # Запускаем таймер на 60 секунд
        self.remaining_time = 60
        self.timer_label.config(text="01:00", foreground="black")
        self.start_time = time.time()

        if self.timer_job:
            self.after_cancel(self.timer_job)
        self.update_timer()

    def update_timer(self):
        """Обновление таймера каждую секунду"""
        if self.remaining_time > 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

            if self.remaining_time <= 10:
                self.timer_label.config(foreground="red")

            self.remaining_time -= 1
            self.timer_job = self.after(1000, self.update_timer)
        else:
            self.finish_training()

    def on_key_release(self, event=None):
        """Проверка введённого текста при каждом нажатии"""
        typed = self.entry.get("1.0", "end-1c")
        self.total_chars_typed = len(typed)

        # Убираем все теги
        self.entry.tag_remove("correct", "1.0", "end")
        self.entry.tag_remove("error", "1.0", "end")

        self.correct_chars = 0
        for i, char in enumerate(typed):
            if i < len(self.current_text) and char == self.current_text[i]:
                self.entry.tag_add("correct", f"1.0 + {i} chars", f"1.0 + {i + 1} chars")
                self.correct_chars += 1
            else:
                self.entry.tag_add("error", f"1.0 + {i} chars", f"1.0 + {i + 1} chars")

        # Обновляем скорость (знаков в минуту)
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            wpm = int(self.correct_chars / elapsed * 60)
            self.speed_label.config(text=f"{wpm} зн/мин")

        # Если текст набран полностью
        if typed == self.current_text:
            self.finish_training(success=True)

    def finish_training(self, success=False):
        """Завершение раунда"""
        if self.timer_job:
            self.after_cancel(self.timer_job)

        self.entry.config(state="disabled")

        if success:
            self.timer_label.config(text="ОТЛИЧНО!", foreground="green")
        else:
            self.timer_label.config(text="ВРЕМЯ ВЫШЛО", foreground="red")

        # Финальная скорость
        elapsed = max(time.time() - self.start_time, 1)
        final_wpm = int(self.correct_chars / elapsed * 60)
        self.speed_label.config(text=f"Финал: {final_wpm} зн/мин")

    @staticmethod
    def _configure_style(style: ttk.Style):
        pass

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
