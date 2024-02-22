from buttons.reply.buttons import start_btn
from database.db_models import User, create_user
from loader import bot


@bot.message_handler(commands=["*", "start", "back"])
def bot_start(message):
    """ф-я регистрирует нового пользователя и приветсвует его"""
    if User.get_or_none(User.user_id == message.from_user.id) is None:
        create_user(message)
        bot.send_message(
            message.chat.id,
            text="Привет, я - бот по поиску отелей с различными функциями",
        )
    else:
        user_data = User.get(User.user_id == message.from_user.id)
        bot.send_message(
            message.chat.id, "Приветствую вас {}".format(user_data.first_name)
        )

    bot.send_message(
        message.chat.id,
        text="Вводите данные очень внимательно, потому что при ошибке придётся начать с самого начала",
        reply_markup=start_btn(),
    )
