from buttons.reply.buttons import cancel_btn
from loader import bot
from scripts.scripts_func import correct_date_input, get_curr_state
from states.states import MyStates


@bot.message_handler(func=lambda message: get_curr_state(message) == MyStates.low_value)
def low_value_input(message):
    """сохраняет нижнее значение для кастомного поиска"""
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_search"]["low_value"] = message.text
    bot.send_message(
        message.chat.id, "Введите верхнюю планку", reply_markup=cancel_btn()
    )
    bot.set_state(message.from_user.id, MyStates.high_value, message.chat.id)


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.high_value
)
def high_value_input(message):
    """сохраняет верхнее значение для кастомного поиска"""
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_search"]["high_value"] = message.text
    bot.send_message(
        message.chat.id,
        "Введите дату прибытия в формате ГГГГ ММ ДД",
        reply_markup=cancel_btn(),
    )
    bot.set_state(message.from_user.id, MyStates.arr_date_input, message.chat.id)


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.arr_date_input
)
def arr_date(message):
    """сохраняет дату прибытия для кастомного поиска"""
    if correct_date_input(message.text):
        with bot.retrieve_data(message.from_user.id) as data:
            data["new_search"]["arrival_date"] = message.text
        bot.send_message(
            message.chat.id,
            "Введите дату отбытия в формате ГГГГ ММ ДД",
            reply_markup=cancel_btn(),
        )
        bot.set_state(
            message.from_user.id, MyStates.departure_date_input, message.chat.id
        )
    else:
        bot.send_message(
            message.chat.id,
            "Вы ввели неверную дату\nВведите дату прибытия в формате ГГГГ ММ ДД",
            reply_markup=cancel_btn(),
        )


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.departure_date_input
)
def dep_date(message):
    """сохраняет дату отбытия для кастомного поиска"""
    if correct_date_input(message.text):
        with bot.retrieve_data(message.from_user.id) as data:
            data["new_search"]["departure_date"] = message.text
        bot.send_message(
            message.chat.id, "Сколько комнат нужно?", reply_markup=cancel_btn()
        )
        bot.set_state(message.from_user.id, MyStates.hotels_amt_input, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            "Вы ввели неверную дату\nВведите дату отбытия в формате ГГГГ ММ ДД",
            reply_markup=cancel_btn(),
        )
