from enums.settings import SettingsParam, Language, Difficulty
from enums.theme_mode import ThemeMode

from config import DATA_DIR_PATH

SETTINGS_FILE_PATH = DATA_DIR_PATH + "settings.json"

DEFAULT_SETTINGS = {
    SettingsParam.LANGUAGE.value: Language.RUSSIAN,
    SettingsParam.DIFFICULTY.value: Difficulty.NORMAL,
    SettingsParam.FONT_SIZE.value: 14,
    SettingsParam.THEME_MODE.value: ThemeMode.DARK
}
