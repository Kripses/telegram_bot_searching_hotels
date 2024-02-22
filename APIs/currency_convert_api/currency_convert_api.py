import requests


def currency_converter(money, currency):
    """ф-я конвертирует валюту в рубли"""
    url = "https://www.cbr-xml-daily.ru/latest.js"

    response = requests.get(url).json()

    return str(round(float(money) / response.get("rates").get(currency), 2))
