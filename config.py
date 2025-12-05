APP_NAME = "ForTrain"

ROUTE_MENU_PATH = "/"
ROUTE_TRAINER = "/game"
ROUTE_SETTINGS = "/settings"

ROUTE_SPECIAL_SYMBOL = "#"
ROUTE_BACK = ROUTE_SPECIAL_SYMBOL + "back"

DEFAULT_JSON_INDENT = 3

DATA_DIR_PATH = "./data/"

STYLES_DIR_PATH = DATA_DIR_PATH + "styles/"
MAIN_STYLE_PATH = STYLES_DIR_PATH + "main.json"
MENU_STYLE_PATH = STYLES_DIR_PATH + "menu.json"
TRAINER_STYLE_PATH = STYLES_DIR_PATH + "trainer.json"
SETTINGS_STYLE_PATH = STYLES_DIR_PATH + "settings.json"

WORDS_DIR_PATH = DATA_DIR_PATH + "words/"
RUSSIAN_WORDS_PATH = WORDS_DIR_PATH + "russian.txt"
ENGLISH_WORDS_PATH = WORDS_DIR_PATH + "english.txt"

SPLIT_CHARS = [" ", ".", ",", ";", "!", "?"]


RUSSIAN_WORDS_REGEX = r"[А-ЯЁа-яё0-9.,!?;:'\"()[\]{}<>\/\\|@#$%^&*_=+~`№-]+"
ENGLISH_WORDS_REGEX = r"[A-Za-z0-9.,!?;:'\"()[\]{}<>\/\\|@#$%^&*_=+~`№-]+"
MIX_WORDS_REGEX = r"[А-ЯЁа-яёA-Za-z0-9.,!?;:'\"()[\]{}<>\/\\|@#$%^&*_=+~`№-]+"
