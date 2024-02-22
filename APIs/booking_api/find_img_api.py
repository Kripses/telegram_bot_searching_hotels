import requests
from config_data.config import BOOKING_KEY


def hotel_img(hotel_id):
    """ф-я ищет фото по id отеля из api booking"""
    url = "https://apidojo-booking-v1.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"hotel_ids": hotel_id, "languagecode": "en-us"}
    headers = BOOKING_KEY

    # headers = {
    #     "X-RapidAPI-Key": "7736209eeemsh679b6b86830acfep13c735jsnf4903e8dbe38",
    #     "X-RapidAPI-Host": "apidojo-booking-v1.p.rapidapi.com"
    # }

    response = requests.get(url, headers=headers, params=querystring).json()
    print(response)

    img_list = [
        response.get("url_prefix") + elem[-4]
        for elem in response.get("data").get(hotel_id)
    ]

    return img_list[0:3]
