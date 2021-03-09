import requests


class NewsService:

    """
    Der News Service liefert einen Array mit entweder einer Liste an zur Verfügung stehenden Sources oder ein
    Array mit zwei Listen bestehend aus den Headlines und den jeweiligen Bild URL's.

    Er kann wie folgt beispielhaft angesprochen werden:
    news = NewsService()
    result = news.query('top', 'sports', None, None)
    """

    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        #self.base_url = 'http://news-service:5575/rest/api/v1'
        self.base_url = 'http://localhost:5575/rest/api/v1'

    def query(self, type, category=None, search=None, exclude=None):
        """
        :param type: 'top', 'everything', 'sources'
        :param category: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology' or None
        :param search: any key word or None
        :param exclude: any domain (bild.de) or None
        :return: array([list_of_headlines],[list_of_img_urls]) or array(list_of_sources)
        """

        article_img = []
        article_headline = []

        if type == 'top':
            result = self.getTopNews(category)
        elif type == 'everything':
            result = self.getNewsSearch(search, exclude)
        elif type == 'sources':
            result = self.getNewsSources()
            return result
        else:
            return 'Please provide a valid type!'

        news_json = result.json()

        for article in news_json['articles']:
            article_img.append(article['title'])
            article_headline.append(article['urlToImage'])

        news_info = [article_img, article_headline]

        return news_info

    def getTopNews(self, category=None):
        """
        :param category: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology' or None
        :return: array([list_of_headlines],[list_of_img_urls])
        """

        if category is not None:
            news = requests.get(f'{self.base_url}/news/top/category?category={category}')

        else:
            news = requests.get(f'{self.base_url}/news/top')

        return news

    def getNewsSearch(self, search=None, exclude=None):
        """
        :param search: any key word or None
        :param exclude: any domain (bild.de) or None
        :return: array([list_of_headlines],[list_of_img_urls])
        """

        if search is not None:
            news = requests.get(f'{self.base_url}/news/everything/search?keyWord={search}')
        elif exclude is not None:
            news = requests.get(f'{self.base_url}/news/everything?exclude={exclude}')
        else:
            news = requests.get(f'{self.base_url}/news/everything')

        return news

    def getNewsSources(self):
        """
        :return: array(list_of_sources)
        """

        news = requests.get(f'{self.base_url}/news/sources')

        return news


news = NewsService()
result = news.query('top', 'sports', None, None)
for i in range(0, len(result[0])):
    print(f'{result[0][i]} : {result[1][i]}')
