from buttons.reply.buttons import start_btn
from loader import bot


@bot.message_handler(commands=["*", "cancel"])
def cancel(message):
    bot.send_message(
        message.chat.id, text="Отмена текущей операции", reply_markup=start_btn()
    )
    bot.delete_state(message.from_user.id, message.chat.id)
