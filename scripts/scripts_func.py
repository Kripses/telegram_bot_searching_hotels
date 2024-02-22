import json
from datetime import datetime

import telebot
from APIs.booking_api.find_img_api import hotel_img
from buttons.reply.buttons import cancel_btn
from database.db_models import Search, User
from loader import bot
from states.states import MyStates


def hotels_output(message, result, text="цена за неделю"):
    """ф-я выводит найденные отели в чат"""
    img = hotel_img(result.get("id"))

    if result.get("score") == 0:
        score = "нет результата"
    else:
        score = result.get("score")

    msg_to_photo = "{text}: {price} рублей\nназвание: {name}\nРейтинг: {score}\nадрес: {address}\nдистанция до центра: {dist}".format(
        text=text,
        price=result.get("price"),
        address=result.get("address"),
        name=result.get("name"),
        dist=result.get("distance"),
        score=score,
    )
    bot.send_media_group(
        message.chat.id,
        [telebot.types.InputMediaPhoto(photo, caption=msg_to_photo) for photo in img],
    )


def dump_log_hotels(log_dict):
    """ф-я записи найденных отелей в файл для использования в ф-ии history"""
    with open("log_files/log_hotels.json", "w") as log_file:
        json.dump(log_dict, log_file, indent=4)


def load_log_hotels():
    """ф-я выгружает данные из файла с отелями"""
    with open("log_files/log_hotels.json", "r") as log_file:
        log_dict = json.load(log_file)
        return log_dict


def accost(message, func_name):
    """ф-я приветстиве. срабатывает при вызове некоторых из deafult handlers"""
    if User.get_or_none(User.user_id == message.from_user.id) is not None:
        searching_user = Search.get(Search.user_id == message.from_user.id)
        searching_user.search_func = func_name
        searching_user.save()
        bot.send_message(
            message.chat.id, text="Введите искомый город", reply_markup=cancel_btn()
        )
        bot.set_state(message.from_user.id, MyStates.city_input, message.chat.id)
    else:
        bot.send_message(
            message.chat.id, text="Вы не зарегестрировались нажмите /start"
        )
        bot.delete_state(message.from_user.id, message.chat.id)


def get_curr_state(message):
    """возвращает текущее состояние пользователя"""
    return bot.get_state(message.from_user.id, message.chat.id)


def correct_date_input(date):
    """проверяет на корректность введённой даты пользователем"""
    try:
        datetime.strptime(date, "%Y %m %d")
        print(date)
        return True
    except ValueError:
        return False
