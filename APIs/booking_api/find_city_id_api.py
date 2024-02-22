import requests
from config_data.config import BOOKING_KEY

from ..translate_api.translate_api import translate
from ..wiki_api.wiki_api import true_name


def find_id_ctiy(city, country):
    """ф-я ищет id отелей по стране и городу из api booking"""
    id_list = list()
    url = "https://apidojo-booking-v1.p.rapidapi.com/locations/auto-complete"

    city = true_name(translate(city))
    country = true_name(translate(country))

    querystring = {"text": city, "languagecode": "en-us"}

    # headers = {
    #     "X-RapidAPI-Key": "7736209eeemsh679b6b86830acfep13c735jsnf4903e8dbe38",
    #     "X-RapidAPI-Host": "apidojo-booking-v1.p.rapidapi.com"
    # }
    headers = BOOKING_KEY

    response = requests.get(url, headers=headers, params=querystring).json()
    print(response)

    for id in response:
        if id.get("country") == country and id.get("city_name") != "":
            id_list.append(id.get("dest_id"))

    print(id_list)
    return id_list
