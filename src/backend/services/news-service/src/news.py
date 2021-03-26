import requests
import json

NEWS_BASE_URL = 'https://newsapi.org/v2/'
API_KEY = '4058bc453cba48cc8747d31b5ba3a60e'
COUNTRY = 'de'
LANGUAGE = 'en'

NEWS_EVERYTHING_URL = '{}{}'.format(NEWS_BASE_URL, 'everything')
NEWS_TOP_HEADLINES_URL = '{}{}'.format(NEWS_BASE_URL, 'top-headlines')
NEWS_SOURCES_URL = '{}{}'.format(NEWS_BASE_URL, 'sources')


def top_headlines_category(category=None):
    if category is not None:
        url = '{}?country={}&category={}&apiKey={}'.format(
            NEWS_TOP_HEADLINES_URL, COUNTRY, category, API_KEY
        )
    else:
        url = '{}?country={}&apiKey={}'.format(NEWS_TOP_HEADLINES_URL, COUNTRY, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)


def key_word_search(key=None, source=None):
    if key is not None and source is not None:
        url = '{}?language={}&q={}&sources={}&apiKey={}'.format(
            NEWS_EVERYTHING_URL, LANGUAGE, key, source, API_KEY
        )
    elif key is not None:
        url = '{}?language={}&q={}&apiKey={}'.format(
            NEWS_EVERYTHING_URL, LANGUAGE, key, API_KEY
        )
    else:
        return {'error': 'Key word invalid!'}
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)


def everything_news(source=None):
    if source is not None:
        url = '{}?language={}&sources={}&apiKey={}'.format(
            NEWS_EVERYTHING_URL, LANGUAGE, source, API_KEY
        )
    else:
        url = '{}?language={}&apiKey={}'.format(NEWS_EVERYTHING_URL, LANGUAGE, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)


def find_sources():
    url = '{}?language={}&apiKey={}'.format(NEWS_SOURCES_URL, LANGUAGE, API_KEY)
    result = requests.get(url).json()
    return json.dumps(result, sort_keys=True, indent=4)
