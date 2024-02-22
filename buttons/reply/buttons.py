from telebot import types


def start_btn():
    """кнопки для ф-ии start"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    low_btn = types.KeyboardButton("/low")
    high_btn = types.KeyboardButton("/high")
    custom_btn = types.KeyboardButton("/custom")
    history_btn = types.KeyboardButton("/history")
    cancel_btn = types.KeyboardButton("/cancel")
    markup.add(low_btn, high_btn, custom_btn, history_btn, cancel_btn)
    return markup


def cancel_btn():
    """кнопка отмены операции"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_btn = types.KeyboardButton("/cancel")
    markup.add(cancel_btn)
    return markup


def sort_mode_btn():
    """кнопки выбора метода сортировки"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    price_btn = types.KeyboardButton("цена")
    dist_btn = types.KeyboardButton("дистанция")
    score_btn = types.KeyboardButton("рейтинг")
    cancel_btn = types.KeyboardButton("/cancel")
    markup.add(price_btn, dist_btn, score_btn, cancel_btn)
    return markup
