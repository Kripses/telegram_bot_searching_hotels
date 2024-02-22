from loader import bot
from scripts.scripts_func import accost


@bot.message_handler(commands=["*", "low"])
def low_func(message):
    accost(message, "low")
