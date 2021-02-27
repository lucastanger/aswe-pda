import requests
import json

NEWS_BASE_URL = "https://newsapi.org/v2/"
API_KEY = "4058bc453cba48cc8747d31b5ba3a60e"
COUNTRY = "de"

NEWS_EVERYTHING_URL = "{}{}".format(NEWS_BASE_URL, "everything")
NEWS_TOP_HEADLINES_URL = "{}{}".format(NEWS_BASE_URL, "top-headlines")
NEWS_SOURCES_URL = "{}{}".format(NEWS_BASE_URL, "sources")


def topHeadlines(category):
    url = "{}?country={}&category={}&apiKey={}".format(NEWS_TOP_HEADLINES_URL, COUNTRY, category, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)


def keyWordSearch(keyWord):
    url = "{}?language={}&q={}&apiKey={}".format(NEWS_EVERYTHING_URL, COUNTRY, keyWord, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)


def findSources():
    url = "{}?country={}&apiKey={}".format(NEWS_SOURCES_URL, COUNTRY, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)

