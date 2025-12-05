import re
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import random

from frames.base import BaseFrame
from enums.route import Route
from enums.settings import Difficulty, Language
from settings import Settings
from config import APP_NAME, MENU_STYLE_PATH, RUSSIAN_WORDS_PATH, RUSSIAN_WORDS_REGEX, \
    ENGLISH_WORDS_PATH, ENGLISH_WORDS_REGEX, MIX_WORDS_REGEX
from utils.storage import load_txt
from utils.text_files import load_text_from_file_with_regex

RUS_TO_LAT = {
    "а": "a", "А": "A",
    "е": "e", "Е": "E",
    "о": "o", "О": "O",
    "с": "c", "С": "C",
    "р": "p", "Р": "P",
    "у": "y", "К": "K",
    "х": "x", "Х": "X",
    "Т": "T", "Н": "H",
    "В": "B"
}

CONFUSABLES = RUS_TO_LAT.copy()

CONFUSABLES.update({v: k for k, v in RUS_TO_LAT.items()})

LAT_TO_RUS = {v: k for k, v in RUS_TO_LAT.items()}

SPLIT_CHARS = [" ", ".", ",", ";", "!", "?"]


class TextGenerator:
    def __init__(
            self,
            language: Language,
            text: Optional[str] = None,
            max_len: Optional[int] = 50,
            symbols: bool = False,
            letters: bool = False,
            register: bool = False
    ):
        self.__language = language
        self.__text = text
        self.__max_len = max_len
        self.__symbols = symbols
        self.__letters = letters
        self.__register = register

    @property
    def text(self) -> list[str]:
        if not self.__text:
            self.generate_text()
        else:
            if self.__language is Language.RUSSIAN:
                regex_prompt = RUSSIAN_WORDS_REGEX
            elif self.__language is Language.ENGLISH:
                regex_prompt = ENGLISH_WORDS_REGEX
            else:
                regex_prompt = MIX_WORDS_REGEX

            self.__text = " ".join(re.findall(re.compile(regex_prompt), self.__text))

        if self.__symbols:
            self.__generate_symbols()

        if self.__register:
            self.__generate_register()

        return self.__split_text()

    def generate_text(self):
        target_len = random.randrange(125, 250)

        if self.__letters:
            join_symbol = ""
        else:
            join_symbol = " "

        if self.__language is Language.RUSSIAN:
            words = load_text_from_file_with_regex(RUSSIAN_WORDS_PATH, RUSSIAN_WORDS_REGEX)
        elif self.__language is Language.ENGLISH:
            words = load_text_from_file_with_regex(ENGLISH_WORDS_PATH, ENGLISH_WORDS_REGEX)
        else:
            words = load_text_from_file_with_regex(RUSSIAN_WORDS_PATH, RUSSIAN_WORDS_REGEX) + \
                    load_text_from_file_with_regex(ENGLISH_WORDS_PATH, ENGLISH_WORDS_REGEX)

        result = []

        while sum(len(w) for w in result) + len(result) - 1 < target_len:
            word = random.choice(words)

            if self.__letters:
                result.append(random.choice(word))
            else:
                result.append(word)

        result = [r.strip() for r in result]

        self.__text = join_symbol.join(result)

    def __generate_symbols(self):
        symbols = '!"№;%:?*()'
        result = []

        for ch in self.__text:
            result.append(ch)
            if random.random() < 0.25:
                for _ in range(random.randint(1, 2)):
                    result.append(random.choice(symbols))

        self.__text = "".join(result)

    def __generate_register(self):
        self.__text = "".join(
            ch.upper() if ch.isalpha() and random.random() < 0.5 else ch.lower()
            if ch.isalpha() else ch
            for ch in self.__text
        )

    def __split_text(self) -> list[str]:
        result = []
        index = 0
        letter = self.__max_len

        while index < len(self.__text):
            chunk = self.__text[index:index + letter]
            cut_pos = None

            for idx in range(len(chunk) - 1, -1, -1):
                if chunk[idx] in SPLIT_CHARS:
                    cut_pos = idx + 1
                    break

            if cut_pos is None:
                part = chunk
                index += letter
            else:
                part = chunk[:cut_pos]
                index += cut_pos

            result.append(part)

        for line_index in range(len(result)):
            line = result[line_index]

            while "  " in line:
                line = line.replace("  ", " ")

            result[line_index] = line.strip()

        return result


class TextSwapper:
    def __init__(self, text: list[str]):
        self.__text = text
        self.__current_index = 0
        self.__max_index = len(text) - 1

    @property
    def current(self) -> Optional[str]:
        if self.__current_index > self.__max_index:
            return None

        return self.__text[self.__current_index]

    @property
    def next(self) -> Optional[str]:
        if self.__current_index > self.__max_index:
            return None

        line = self.__text[self.__current_index]
        self.__current_index += 1

        return line

    @property
    def index_decorated(self) -> str:
        return f"{self.__current_index}/{self.__max_index + 1}"


class TrainerFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, f"{APP_NAME} - Тренажёр")

        self.__settings: Settings = self._controller.settings

        self.__countdown_label = None
        self.__elapsed_label = None
        self.__upload_text_btn = None
        self.__text_swapper = None
        self.__text_display = None

        self.__current_line = ""
        self.__typed_text = ""
        self.__errors = 0
        self.__correct_chars_typed_in_previous_lines = 0
        self.__countdown_running = False
        self.__countdown_time_total: Optional[int] = None
        self.__countdown_time_left: Optional[int] = None
        self.__elapsed_running = False
        self.__elapsed_start = None

        self.__entry = None
        self.__stats_label = None

    @property
    def content(self) -> ttk.Frame:
        frame = ttk.Frame(self._parent)

        font_size = self.__settings.font_size

        header = ttk.Frame(frame, height=50)
        header.pack(fill="x")

        self.__countdown_label = ttk.Label(header, text="01:00", font=("Segue UI", 25))
        self.__countdown_label.pack_forget()

        self.__elapsed_label = ttk.Label(header, text="00:00", font=("Segue UI", 14))
        self.__elapsed_label.pack_forget()

        header_buttons = ttk.Frame(header)
        header_buttons.pack(side="right", padx=20)

        ttk.Button(
            header_buttons,
            text="ОБНОВИТЬ",
            command=lambda: self.__update_text_display(),
            style="TrainerHeader.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            header_buttons,
            text="В МЕНЮ",
            command=lambda: self._controller.go(Route.ROUTE_MENU),
            style="TrainerHeader.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            header_buttons,
            text="НАСТРОЙКИ",
            command=lambda: self._controller.go(Route.ROUTE_SETTINGS),
            style="TrainerHeader.TButton"
        ).pack(side="left", padx=5)

        self.__upload_text_btn = ttk.Button(
            header_buttons,
            width=20,
            text="ЗАГРУЗИТЬ ТЕКСТ",
            style="TrainerHeader.TButton",
            command=lambda: self.__upload_own_text()
        )
        self.__upload_text_btn.pack_forget()

        self.__text_display = tk.Text(
            frame,
            font=("Segoe UI", font_size),
            bg=self._parent.cget("bg"),
            borderwidth=0,
            height=1,
            wrap="word",
            bd=0,
            highlightthickness=0
        )
        self.__text_display.pack(pady=(0, 25), fill="x", expand=True)
        self.__text_display.tag_configure("center", justify="center")
        self.__text_display.config(state="disabled")

        self.__entry = tk.Entry(frame, font=("Segoe UI", font_size), width=50)
        self.__entry.pack()
        self.__entry.bind("<KeyRelease>", self.__check_input)

        self.__stats_label = ttk.Label(frame, text="", font=("Segoe UI", 14)) # Ошибки: 0
        self.__stats_label.pack(pady=10)

        self.__prepare_ui()
        self.__update_text_display()

        return frame

    def __prepare_ui(self):
        if self.__settings.on_time:
            self.__countdown_label.pack(side="left", padx=(0, 25))

        # self.__elapsed_label.pack(side="left", padx=(0, 10))

        if self.__settings.difficulty in [Difficulty.EASY, Difficulty.NORMAL]:
            self.__upload_text_btn.pack(side="left", padx=5)

    def __update_text_display(self, text: Optional[str] = None):
        generated_text = TextGenerator(
            self.__settings.language,
            text,
            symbols=self.__settings.difficulty in [Difficulty.HARD, Difficulty.INSANE],
            letters=self.__settings.difficulty in [Difficulty.HARD, Difficulty.INSANE],
            register=self.__settings.difficulty in [Difficulty.NORMAL, Difficulty.INSANE]
        ).text

        self.__text_swapper = TextSwapper(generated_text)

        self.__countdown_running = False

        self.__elapsed_running = False

        self.__elapsed_start = None

        self.__correct_chars_typed_in_previous_lines = 0

        total_seconds = max(1, int(sum(len(inner) for inner in generated_text)))

        if self.__settings.difficulty is Difficulty.EASY:
            total_seconds = int(total_seconds * 0.85)
        elif self.__settings.difficulty is Difficulty.NORMAL:
            total_seconds = int(total_seconds * 0.75)
        elif self.__settings.difficulty is Difficulty.HARD:
            total_seconds = int(total_seconds * 0.5)
        else:
            total_seconds = int(total_seconds * 0.25)

        self.__countdown_time_total = total_seconds
        self.__countdown_time_left = total_seconds

        self.__update_stats()

        self.__text_display_next()

    def __text_display_next(self):
        current = self.__text_swapper.current

        if current is not None:
            self.__correct_chars_typed_in_previous_lines += len(current)

        text = self.__text_swapper.next

        if text is None:
            self.__finish()

            return

        self.__current_line = text if text else ""

        self.__entry.delete(0, "end")
        self.__typed_text = ""
        self.__errors = 0

        self.__draw_colored_text("")
        self.__update_time_labels()

    def __draw_colored_text(self, typed: str):
        self.__text_display.config(state="normal")

        self.__text_display.delete("1.0", "end")

        line = self.__current_line

        for i, ch in enumerate(line):
            if i < len(typed):
                if self.__chars_match(ch, typed[i]):
                    self.__text_display.insert("end", ch, "correct")
                else:
                    self.__text_display.insert("end", typed[i] if typed[i] != " " else "_", "wrong")
            elif i == len(typed):
                if len(typed) > 0 and ch.strip():
                    self.__text_display.insert("end", ch, "active")
                else:
                    self.__text_display.insert("end", ch)
            else:
                self.__text_display.insert("end", ch)

        self.__text_display.tag_config("correct", foreground="green")
        self.__text_display.tag_config("wrong", foreground="red")
        self.__text_display.tag_config("active", background="blue")
        self.__text_display.tag_add("center", "1.0", "end")

        self.__text_display.config(state="disabled")

    def __chars_match(self, expected: str, typed: str) -> bool:
        """
        Возвращает True, если символы совпадают точно или визуально
        (а/a, о/o, т/m и т.д. — всегда засчитывается, независимо от языка)
        """
        if not expected or not typed:
            return False

        # Точное совпадение
        if expected == typed:
            return True

        # Визуальное совпадение по твоей таблице — в любую сторону
        return CONFUSABLES.get(expected) == typed

    def __check_input(self, event):
        typed = self.__entry.get()

        self.__typed_text = typed

        if not self.__elapsed_running and typed:
            self.__elapsed_start = time.time()
            self.__elapsed_running = True
            self.__update_elapsed_label()

        if self.__settings.on_time and not self.__countdown_running and typed:
            self.__countdown_running = True
            self.__update_countdown()

        self.__errors = sum(
            1 for i in range(len(typed))
            if i < len(self.__current_line) and not self.__chars_match(self.__current_line[i], typed[i])
        )

        self.__draw_colored_text(typed)

        self.__update_stats()

        if len(typed) == len(self.__current_line) and all(
                self.__chars_match(self.__current_line[i], typed[i]) for i in range(len(self.__current_line))
        ):
            self.__text_display_next()

    def __update_countdown(self):
        if not self.__countdown_running or not self.__settings.on_time:
            return

        if self.__countdown_time_left is None:
            self.__countdown_time_left = 60

        self.__countdown_time_left -= 1

        if self.__countdown_time_left <= 0:
            try:
                self.__countdown_label.config(text="00:00")
            except Exception as ex:
                pass

            self.__countdown_running = False

            self.__finish(time_is_up=True)

            return

        minutes = self.__countdown_time_left // 60
        seconds = self.__countdown_time_left % 60

        try:
            self.__countdown_label.config(text=f"{minutes:02}:{seconds:02}")
        except Exception:
            pass

        self._parent.after(1000, self.__update_countdown)

    def __update_elapsed_label(self):
        if not self.__elapsed_running:
            return

        elapsed = int(time.time() - self.__elapsed_start)
        minutes = elapsed // 60
        seconds = elapsed % 60

        try:
            self.__elapsed_label.config(text=f"{minutes:02}:{seconds:02}")
        except Exception:
            pass

        self._parent.after(250, self.__update_elapsed_label)

    def __update_time_labels(self):
        if self.__settings.on_time and self.__countdown_time_left is not None:
            minutes = self.__countdown_time_left // 60
            seconds = self.__countdown_time_left % 60

            self.__countdown_label.config(text=f"{minutes:02}:{seconds:02}")
        else:
            self.__countdown_label.config(text="")
        if self.__elapsed_running and self.__elapsed_start is not None:
            elapsed = int(time.time() - self.__elapsed_start)

            minutes = elapsed // 60
            seconds = elapsed % 60

            self.__elapsed_label.config(text=f"{minutes:02}:{seconds:02}")
        else:
            self.__elapsed_label.config(text="00:00")

    def __finish(self, time_is_up=False):
        if self.__elapsed_running:
            used_time = time.time() - self.__elapsed_start
        else:
            if self.__settings.on_time and self.__countdown_time_total is not None:
                used_time = self.__countdown_time_total - (self.__countdown_time_left or 0)
            else:
                used_time = 0

        used_time = max(used_time, 1)
        correct_chars = sum(
            1 for i in range(min(len(self.__typed_text), len(self.__current_line)))
            if self.__chars_match(self.__current_line[i], self.__typed_text[i])
        )

        cpm = int((self.__correct_chars_typed_in_previous_lines + correct_chars) / used_time * 60)
        wpm = int(cpm / 5)

        if time_is_up:
            result_msg = "Время вышло!"
        else:
            result_msg = "Готово!"

        self.__countdown_running = False

        messagebox.showinfo(
            result_msg,
            # f"Ошибки: {self.__errors}\n"
            f"Время: {used_time:.2f} сек\n"
            f"Скорость:\n{cpm} CPM\n{wpm} WPM"
        )

        self.__update_text_display()

    def __update_stats(self):
        if self.__elapsed_running and self.__elapsed_start is not None:
            elapsed = time.time() - self.__elapsed_start
        else:
            elapsed = 0

        elapsed = max(elapsed, 1)

        correct_chars = sum(
            1 for i in range(min(len(self.__typed_text), len(self.__current_line)))
            if self.__chars_match(self.__current_line[i], self.__typed_text[i])
        )

        cpm = int((self.__correct_chars_typed_in_previous_lines + correct_chars) / elapsed * 60) if correct_chars > 0 else 0
        wpm = int(cpm / 5)

        self.__stats_label.config(text=f"{self.__text_swapper.index_decorated}   CPM: {cpm}   WPM: {wpm}") # Ошибки: {self.__errors}

    def __upload_own_text(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", "*.txt")]
        )

        if file_path:
            try:
                text = load_txt(file_path)

                self.__update_text_display(text)
            except Exception as ex:
                self._controller.show_error("Ошибка при открытии файла.", f"Не удалось открыть файл {file_path}.\nТекст ошибки:{ex}.")

    def _configure_style(self, style: ttk.Style):
        self._controller.configure_style_by_path(style, MENU_STYLE_PATH)

    def refresh(self, style: ttk.Style):
        self._configure_style(style)
