from loader import bot
from scripts.scripts_func import accost


@bot.message_handler(commands=["*", "custom"])
def high_func(message):
    accost(message, "custom")
