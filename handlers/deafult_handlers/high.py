from loader import bot
from scripts.scripts_func import accost


@bot.message_handler(commands=["*", "high"])
def high_func(message):
    accost(message, "high")
