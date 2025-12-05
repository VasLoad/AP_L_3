from typing import Any

from enums.settings import SettingsParam, Language, Difficulty, Challenges
from enums.theme_mode import ThemeMode

from utils.validators import enum_value_validator, num_validator

from config import DATA_DIR_PATH

MIN_FONT_SIZE = 12
MAX_FONT_SIZE = 34

SETTINGS_FILE_PATH = DATA_DIR_PATH + "settings.json"

DEFAULT_LANGUAGE_PARAM_VALUE = Language.RUSSIAN
DEFAULT_DIFFICULTY_PARAM_VALUE = Difficulty.NORMAL
DEFAULT_FONT_SIZE_PARAM_VALUE = MAX_FONT_SIZE
DEFAULT_THEME_MODE_PARAM_VALUE = ThemeMode.DARK
DEFAULT_ON_TIME_PARAM_VALUE = True
DEFAULT_CHALLENGES_PARAM_VALUE = {
    Challenges.ON_TIME.value: DEFAULT_ON_TIME_PARAM_VALUE
}

DEFAULT_SETTINGS = {
    SettingsParam.LANGUAGE.value: DEFAULT_LANGUAGE_PARAM_VALUE,
    SettingsParam.DIFFICULTY.value: DEFAULT_DIFFICULTY_PARAM_VALUE,
    SettingsParam.FONT_SIZE.value: DEFAULT_FONT_SIZE_PARAM_VALUE,
    SettingsParam.THEME_MODE.value: DEFAULT_THEME_MODE_PARAM_VALUE,
    SettingsParam.CHALLENGES.value: DEFAULT_CHALLENGES_PARAM_VALUE
}


class Settings:
    def __init__(self, settings: dict[str, Any]):
        self.__language = settings.get(SettingsParam.LANGUAGE.value)

        if enum_value_validator(self.__language, Language):
            self.__language = Language(self.__language)
        else:
            self.__language = DEFAULT_LANGUAGE_PARAM_VALUE

        self.__difficulty = settings.get(SettingsParam.DIFFICULTY.value)

        if enum_value_validator(self.__difficulty, Difficulty):
            self.__difficulty = Difficulty(self.__difficulty)
        else:
            self.__difficulty = DEFAULT_DIFFICULTY_PARAM_VALUE

        self.__theme_mode = settings.get(SettingsParam.THEME_MODE.value)

        if enum_value_validator(self.__theme_mode, ThemeMode):
            self.__theme_mode = ThemeMode(self.__theme_mode)
        else:
            self.__theme_mode = DEFAULT_THEME_MODE_PARAM_VALUE

        self.__font_size = settings.get(SettingsParam.FONT_SIZE.value)

        self.__font_size = num_validator(self.__font_size, MIN_FONT_SIZE, MAX_FONT_SIZE)

        challenges = settings.get(SettingsParam.CHALLENGES.value, DEFAULT_CHALLENGES_PARAM_VALUE)

        self.__on_time = challenges.get(Challenges.ON_TIME.value)

        if not isinstance(self.__on_time, bool):
            self.__on_time = DEFAULT_ON_TIME_PARAM_VALUE

    @property
    def language(self) -> Language:
        return self.__language

    @property
    def difficulty(self) -> Difficulty:
        return self.__difficulty

    @property
    def theme_mode(self) -> ThemeMode:
        return self.__theme_mode

    @property
    def font_size(self):
        return self.__font_size

    @property
    def challenges(self) -> dict[str, Any]:
        return {
            Challenges.ON_TIME.value: self.on_time
        }

    @property
    def on_time(self) -> bool:
        return self.__on_time

    @property
    def json(self) -> dict[str, Any]:
        return {
            SettingsParam.LANGUAGE.value: self.language,
            SettingsParam.DIFFICULTY.value: self.difficulty,
            SettingsParam.FONT_SIZE.value: self.font_size,
            SettingsParam.CHALLENGES.value: {
                Challenges.ON_TIME.value: self.on_time
            }
        }
