import json
import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOOKING_KEY = json.loads(os.getenv("BOOKING_KEY"))
TRANSLATE_KEY = json.loads(os.getenv("TRANSLATE_KEY"))
WIKI_KEY = json.loads(os.getenv("WIKI_KEY"))
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("low", "Сортирует по возрастанию"),
    ("high", "Сортирует по убыванию"),
    ("custom", "Ищет по большему кол-ву параметров"),
    ("history", "Выдаёт историю последних 10 запросов"),
)
