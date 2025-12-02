from enum import Enum, StrEnum
from typing import Optional

class SettingsParam(Enum):
    LANGUAGE = "language"
    DIFFICULTY = "difficulty"
    THEME_MODE = "theme_mode"
    FONT_SIZE = "font_size"
    CHALLENGES = "challenges"

class Language(StrEnum):
    RUSSIAN = "russian"
    ENGLISH = "english"
    MIX = "mix"

    def __str__(self):
        return self.label

    @property
    def label(self) -> Optional[str]:
        labels = {
            self.RUSSIAN: "Русский",
            self.ENGLISH: "Английский",
            self.MIX: "Смешанный"
        }

        return labels.get(self)


class Difficulty(StrEnum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    INSANE = "insane"

    def __str__(self):
        return self.label

    @property
    def label(self) -> Optional[str]:
        labels = {
            self.EASY: "Легко",
            self.NORMAL: "Нормально",
            self.HARD: "Сложно",
            self.INSANE: "Безумно"
        }

        return labels.get(self)


class Challenges(StrEnum):
    ON_TIME = "on_time"

    def __str__(self):
        return self.label

    @property
    def label(self) -> Optional[str]:
        labels = {
            self.ON_TIME: "На время"
        }

        return labels.get(self)
