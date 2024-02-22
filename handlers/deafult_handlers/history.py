from buttons.reply.buttons import cancel_btn
from database.db_models import Search
from loader import bot
from scripts.scripts_func import get_curr_state, hotels_output, load_log_hotels
from states.states import MyStates


@bot.message_handler(commands=["*", "history"])
def history_func(message):
    """функция хэндлер для вывода 10 последних запросов(формирования строки)"""
    searching_user = Search.get(Search.user_id == message.from_user.id)
    searching_user.search_func = "history"
    searching_user.save()

    log_hotels = load_log_hotels().get(str(message.from_user.id))

    @bot.message_handler(
        func=lambda message: get_curr_state(message) == MyStates.history
    )
    def history_req_output(message):
        """ф-ия выводит в чат отели по выбранному номеру из предыдущего пункта"""
        try:
            if len(log_hotels[int(message.text) - 1][1]) == 0:
                raise TypeError
            for result in log_hotels[int(message.text) - 1][1]:
                if searching_user.search_func == "custom":
                    hotels_output(message, result, "цена за указанный вами период")
                else:
                    hotels_output(message, result)
            bot.delete_state(message.from_user.id, message.chat.id)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "Вы ввели не число\nНапишите номер интересующего запроса",
            )
        except IndexError:
            bot.send_message(
                message.chat.id,
                "Вы ввели несуществующий запрос\nНапишите номер интересующего запроса",
            )
        except TypeError:
            bot.send_message(
                message.chat.id,
                "Упс, кажется по этому запросу ничего не было найдено\nНапишите номер интересующего запроса",
            )

    bot_msg = ""
    for index, hotel in enumerate(log_hotels):
        bot_msg += "{index} запрос:\n\tГород: {city}\n\tСтрана: {country}\n\tКол-во комнат: {room_amt}\n\tМетод поиска: {search_func}\n".format(
            index=index + 1,
            city=hotel[0].get("city"),
            country=hotel[0].get("country"),
            room_amt=hotel[0].get("room_amt"),
            search_func=hotel[0].get("search_func"),
        )

    bot.send_message(message.chat.id, text=bot_msg)
    bot.send_message(
        message.chat.id,
        text="Напишите номер интересующего запроса",
        reply_markup=cancel_btn(),
    )
    bot.set_state(message.from_user.id, MyStates.history, message.chat.id)
