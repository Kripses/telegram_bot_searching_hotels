from datetime import datetime

import requests
from config_data.config import BOOKING_KEY
from scripts.scripts_without_error import city_country_rename, custom_sort

from ..currency_convert_api.currency_convert_api import currency_converter


def hotel_search(
    dest_ids,
    sort_mode,
    result_amt,
    search_mode,
    city,
    country,
    arrival_date,
    departure_date,
    room_amt,
    message,
):
    """ищет отели через api booking по заданным ранее параметрам
    , и сортирует результат по выбранной функции поиска"""
    url = "https://apidojo-booking-v1.p.rapidapi.com/properties/list"
    city_country = city_country_rename(city, country)

    if departure_date is None:
        arrival_date = date_time()
        departure_date = date_time(True)
        print(arrival_date, departure_date)

    if "-" not in arrival_date:
        arrival_date = date_rework(arrival_date)
        departure_date = date_rework(departure_date)
        print(room_amt, arrival_date, departure_date)

    finded_hotel = list()

    for dest_id in dest_ids:
        print(dest_id)
        querystring = {
            "offset": "0",
            "arrival_date": arrival_date,
            "departure_date": departure_date,
            "guest_qty": "1",
            "dest_ids": dest_id,
            "room_qty": room_amt,
            "search_type": "city",
            "children_qty": "0",
            "search_id": "none",
            "price_filter_currencycode": "USD",
            "order_by": "popularity",
            "languagecode": "en-us",
            "travel_purpose": "leisure",
        }

        # headers = {
        #     "X-RapidAPI-Key": "7736209eeemsh679b6b86830acfep13c735jsnf4903e8dbe38",
        #     "X-RapidAPI-Host": "apidojo-booking-v1.p.rapidapi.com"
        # }
        headers = BOOKING_KEY

        response = requests.get(url, headers=headers, params=querystring).json()
        print(response)

        try:
            for res_amt, result in enumerate(response.get("result")):
                if city_country[0] not in result.get("city_name_en") and city_country[
                    1
                ] not in result.get("country_trans"):
                    continue

                finded_hotel_dict = dict()
                finded_hotel_dict["price"] = currency_converter(
                    result.get("price_breakdown").get("all_inclusive_price"),
                    result.get("currencycode"),
                )
                finded_hotel_dict["main_photo_url"] = result.get("main_photo_url")
                finded_hotel_dict["address"] = result.get("address")
                finded_hotel_dict["name"] = result.get("hotel_name")
                finded_hotel_dict["distance"] = result.get("distance_to_cc")
                finded_hotel_dict["score"] = result.get("review_score")
                finded_hotel_dict["id"] = str(result.get("hotel_id"))

                finded_hotel.append(finded_hotel_dict)
        except TypeError:
            print("TypeError")

    for elem in finded_hotel:
        if elem.get("score") is None:
            elem["score"] = 0

    if search_mode == "low":
        finded_hotel.sort(key=lambda elem: float(elem.get(sort_mode, 0)))
    elif search_mode == "high":
        finded_hotel.sort(key=lambda elem: float(elem.get(sort_mode, 0)), reverse=True)
    elif search_mode == "custom":
        finded_hotel.sort(key=lambda elem: float(elem.get(sort_mode, 0)))
        finded_hotel = custom_sort(message, finded_hotel)

    print(finded_hotel)
    if len(finded_hotel) >= result_amt:
        return finded_hotel[0:result_amt]
    else:
        return finded_hotel


def date_rework(date):
    """приводит дату к видо для использования в api"""
    result = date.replace(" ", "-")
    return result


def date_time(flag=False):
    """если дата не была задана, то создаёт её"""
    raw_date = list(map(int, str(datetime.now()).split(" ")[0].split("-")))
    if raw_date[1] != 12:
        raw_date[1] = raw_date[1] + 1
    else:
        raw_date[1] = 1
    if flag:
        raw_date[2] = 27
    else:
        raw_date[2] = 20
    raw_date = list(map(str, raw_date))
    return "-".join(raw_date)
