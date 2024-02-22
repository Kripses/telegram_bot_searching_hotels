from APIs.translate_api.translate_api import translate
from APIs.wiki_api.wiki_api import true_name
from database.db_models import Search


def city_country_rename(city, country):
    """меняет названия города и страны для работы с api"""
    country = true_name(translate(country))
    city = true_name(translate(city))
    return city, country


def custom_sort(message, hotels):
    """сортирует отели для режима custom"""
    searching_user = Search.get(Search.user_id == message.from_user.id)
    sorted_hotel_for_custom = list()
    for hotel in hotels:
        if (
            float(searching_user.low_value)
            <= float(hotel["price"])
            <= float(searching_user.high_value)
        ):
            sorted_hotel_for_custom.append(hotel)
    else:
        return sorted_hotel_for_custom
