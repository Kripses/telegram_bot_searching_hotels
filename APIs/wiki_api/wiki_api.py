import requests
from config_data.config import WIKI_KEY


def true_name(false_name):
    """приводит страну и город в кононичный для работы с api"""
    url = "https://wiki-briefs.p.rapidapi.com/search"

    querystring = {"q": false_name, "topk": "3"}

    headers = WIKI_KEY

    response = requests.get(url, headers=headers, params=querystring).json()
    print(response.get("title"))

    return response.get("title")
