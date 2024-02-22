import requests
from config_data.config import TRANSLATE_KEY


def translate(word):
    # url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    #
    # headers = {
    #     "content-type": "application/x-www-form-urlencoded",
    #     "Accept-Encoding": "application/gzip",
    #     "X-RapidAPI-Key": "7736209eeemsh679b6b86830acfep13c735jsnf4903e8dbe38",
    #     "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    # }
    #
    # response = requests.post(url, data=payload, headers=headers).json()
    """переводит город и страну на английский для использования в api"""
    url = "https://text-translator2.p.rapidapi.com/translate"

    payload = {"source_language": "ru", "target_language": "en", "text": word}
    headers = TRANSLATE_KEY

    response = requests.post(url, data=payload, headers=headers)
    print(response)
    response = response.json()

    return response.get("data").get("translatedText")
