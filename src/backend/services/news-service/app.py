from flask import Flask, request
from src.news import keyWordSearch, findSources, topHeadlinesCategory, everythingNews

app = Flask(__name__)
app.secret_key = 'some key for session'


@app.route('/rest/api/v1/news/top/')
def general():
    result = topHeadlinesCategory()
    return result


@app.route('/rest/api/v1/news/top/category/')
def top():
    if request.args['category']:
        category = request.args['category']
        result = topHeadlinesCategory(category)
    else:
        return "Please provide a valid category!"
    return result


@app.route('/rest/api/v1/news/everything/')
def everything():
    if request.args['exclude']:
        exclude = request.args['exclude']
        result = everythingNews(exclude)
    else:
        result = everythingNews()
    return result


@app.route('/rest/api/v1/news/everything/search')
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
