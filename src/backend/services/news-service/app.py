from flask import Flask, request
from src.news import keyWordSearch, findSources, topHeadlines

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route('/rest/api/v1/news/top/')
def top():
    if request.args['category']:
        category = request.args['category']
    else:
        return "Please provide a valid category! Possible values are business entertainment general health science sports technology"

    result = topHeadlines(category)
    return result


@app.route('/rest/api/v1/news/search/')
def search():
    if request.args['keyWord']:
        keyWord = request.args['keyWord']
    else:
        return "Please provide a key word by using ?keyWord= at the end of your request!"

    result = keyWordSearch(keyWord)
    return result


@app.route('/rest/api/v1/news/sources/')
def sources():
    result = findSources()
    return result


if __name__ == '__main__':
    app.run(port=5575, host='0.0.0.0')
