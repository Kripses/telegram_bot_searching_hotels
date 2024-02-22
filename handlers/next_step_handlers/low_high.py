from APIs.booking_api.find_city_id_api import find_id_ctiy
from APIs.booking_api.find_hotel_api import hotel_search
from buttons.reply.buttons import cancel_btn, sort_mode_btn
from database import db_models
from loader import bot
from scripts.scripts_func import (dump_log_hotels, get_curr_state,
                                  hotels_output, load_log_hotels)
from states.states import MyStates


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.city_input
)
def city_input(message):
    """ф-я сохраняет id пользователя, поисковую функцию и просит ввести искомую страну"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        searching_user = db_models.Search.get(
            db_models.Search.user_id == message.from_user.id
        )
        data["new_search"] = {
            "user_id": message.from_user.id,
            "search_func": searching_user.search_func,
        }
        data["new_search"]["city_search"] = message.text

    bot.send_message(
        message.chat.id, text="введите искомую страну", reply_markup=cancel_btn()
    )
    bot.set_state(message.from_user.id, MyStates.country_input, message.chat.id)


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.country_input
)
def country_input(message):
    """ф-я сохраняет город и просит выбрать метод будущей сортировки"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["new_search"]["country_search"] = message.text

    global dest_ids
    dest_ids = find_id_ctiy(
        data["new_search"]["city_search"], data["new_search"]["country_search"]
    )
    if len(dest_ids) == 0:
        bot.send_message(
            message.chat.id,
            text="Нет такого городаа или страны:c\nВведите город",
            reply_markup=cancel_btn(),
        )
        bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    else:
        bot.send_message(
            message.chat.id, text="выберите метод поиска", reply_markup=sort_mode_btn()
        )
        bot.set_state(message.from_user.id, MyStates.rooms_amt_input, message.chat.id)


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.rooms_amt_input
)
def rooms_amt_save(message):
    """ф-я сохраняет метод сорировки и просит ввести следуюший параметр (в зависимости от выбранной функции поиска)"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data["new_search"].get("search_mode") is None:
            if message.text == "цена":
                bot.send_message(message.chat.id, "Поиск будет производиться по ценам")
                data["new_search"]["search_mode"] = "price"
            elif message.text == "дистанция":
                bot.send_message(
                    message.chat.id,
                    "Поиск будет производиться по расстоянию от указанного вами города",
                )
                data["new_search"]["search_mode"] = "distance"
            elif message.text == "рейтинг":
                bot.send_message(
                    message.chat.id, "Поиск будет производиться по рейтингу"
                )
                data["new_search"]["search_mode"] = "score"

    if data["new_search"]["search_func"] == "custom":
        bot.send_message(
            message.chat.id, "Введите нижнюю планку", reply_markup=cancel_btn()
        )
        bot.set_state(message.from_user.id, MyStates.low_value, message.chat.id)
    else:
        bot.send_message(
            message.chat.id, "Сколько комнат нужно?", reply_markup=cancel_btn()
        )
        bot.set_state(message.from_user.id, MyStates.hotels_amt_input, message.chat.id)


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.hotels_amt_input
)
def hotels_amt_input(message):
    """ф-я сохраняет кол-во комнат и просит ввести кол-во искомых отелей"""
    try:
        int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["new_search"]["guest_qty"] = message.text

        bot.send_message(
            message.chat.id, "Сколько отелей найти(1-10)?", reply_markup=cancel_btn()
        )
        bot.set_state(
            message.from_user.id, MyStates.log_and_find_hotel, message.chat.id
        )
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели не число\nСколько комнат нужно?")


@bot.message_handler(
    func=lambda message: get_curr_state(message) == MyStates.log_and_find_hotel
)
def log_and_find_hotel(message):
    """ф-я сохраняет кол-во отеллй, ищет их и логирует"""
    if int(message.text) > 10:
        hotel_amt = "10"
    else:
        hotel_amt = message.text
    bot.send_message(message.chat.id, "найду {} отелей".format(int(hotel_amt)))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["new_search"]["hotel_amt_search"] = hotel_amt
    searching_user = db_models.Search(**data["new_search"])
    searching_user.save()
    finded_hotel = hotel_search(
        dest_ids,
        searching_user.search_mode,
        int(searching_user.hotel_amt_search),
        searching_user.search_func,
        searching_user.city_search,
        searching_user.country_search,
        searching_user.arrival_date,
        searching_user.departure_date,
        searching_user.guest_qty,
        message,
    )
    try:
        log_dict = load_log_hotels()
    except FileNotFoundError:
        log_dict = dict()
        dump_log_hotels(log_dict)
    if log_dict.get(str(message.from_user.id)) is None:
        log_dict[str(message.from_user.id)] = list()
    for index, elem in enumerate(log_dict.get(str(message.from_user.id))):
        elem[2] -= 1
    else:
        try:
            if log_dict.get(str(message.from_user.id))[0][2] == 0:
                log_dict.get(str(message.from_user.id)).pop(0)
        except IndexError:
            print("пока логов нет")
        new_log = [
            {
                "city": searching_user.city_search,
                "country": searching_user.country_search,
                "room_amt": searching_user.guest_qty,
                "search_func": searching_user.search_func,
            },
            finded_hotel,
            10,
        ]
        log_dict.get(str(message.from_user.id)).append(new_log)

        dump_log_hotels(log_dict)
    try:
        if len(finded_hotel) == 0:
            raise IndexError
        for result in finded_hotel:
            if searching_user.search_func == "custom":
                hotels_output(message, result, "цена за указанный вами период")
            else:
                hotels_output(message, result)

        bot.delete_state(message.from_user.id, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели не число\nСколько отелей найти?")
    except IndexError:
        bot.send_message(message.chat.id, "Упс, кажетсе мы не нашли ни одного отеля")
        bot.delete_state(message.from_user.id, message.chat.id)
