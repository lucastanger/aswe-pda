from flask import Flask, request
from src.news import (
    key_word_search,
    find_sources,
    top_headlines_category,
    everything_news,
)

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route('/rest/api/v1/news/top')
def general():
    result = top_headlines_category()
    return result


@app.route('/rest/api/v1/news/top/category')
def top():
    if request.args['category']:
        category = request.args['category']
        result = top_headlines_category(category)
    else:
        return 'Please provide a valid category!'
    return result


@app.route('/rest/api/v1/news/everything')
def everything():
    if 'source' in request.args:
        source = request.args['source']
        result = everything_news(source)
    else:
        result = everything_news()
    return result


@app.route('/rest/api/v1/news/everything/search')
def search():
    if 'keyWord' in request.args and 'source' in request.args:
        key = request.args['keyWord']
        source = request.args['source']

        result = key_word_search(key, source)
    elif 'keyWord' in request.args:
        key = request.args['keyWord']

        result = key_word_search(key, None)
    else:
        return (
            'Please provide a key word by using ?keyWord= at the end of your request!'
        )

    return result


@app.route('/rest/api/v1/news/sources')
def sources():
    result = find_sources()
    return result


if __name__ == '__main__':
    app.run(port=5575, host='0.0.0.0')
