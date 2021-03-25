import requests
from pymongo import MongoClient
from dotmap import DotMap

client = MongoClient(host='mongo', port=27017)
db = client['aswe-pda']
db.authenticate('dev', 'dev')
configuration = db['configuration']


class NewsService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://news-service:5575/rest/api/v1'

    def query(self):
        config = configuration.find_one({'news': {'$exists': True}})

        paper_id = config['news']['_papers']
        category = config['news']['_categories']

        papers = self.get_news_source()

        papers_json = papers.json()
        paper_sources = DotMap(papers_json)

        if papers:
            for paper in paper_sources.sources:
                if paper.name == paper_id:
                    paper_id = paper.id

        print(paper_id)

        if 'type' in self.parameters:
            if self.parameters['type'] == 'top':
                if category:
                    result = self.get_top_news(category)
                else:
                    result = self.get_top_news()
            elif self.parameters['type'] == 'everything':
                if 'search' in self.parameters and paper_id:
                    result = self.get_news_search(self.parameters['search'], paper_id)
                elif paper_id:
                    result = self.get_news_search(None, paper_id)
                elif 'search' in self.parameters:
                    result = self.get_news_search(self.parameters['search'], None)
                else:
                    result = self.get_news_search()
            elif self.parameters['type'] == 'sources':
                response = self.get_news_source()

                sources_json = response.json()
                sources = DotMap(sources_json)
                result = []

                if response:
                    for source in sources.sources:
                        result.append(
                            {'name': source.name, 'url': source.url, 'id': source.id}
                        )
            else:
                return 'Please provide a valid type!'
        else:
            return 'Please provide a type!'

        return result

    def get_top_news(self, category=None):
        result = []

        if category is not None:
            for cat in category:
                response = requests.get(
                    f'{self.base_url}/news/top/category?category={cat}'
                )

                result = self.format_news(response, result)
        else:
            response = requests.get(f'{self.base_url}/news/top')

            result = self.format_news(response, result)

        return result

    def get_news_search(self, search=None, source=None):
        result = []

        if search is not None and source is not None:
            response = requests.get(
                f'{self.base_url}/news/everything/search?keyWord={search}&source={source}'
            )

            result = self.format_news(response, result)

        elif source is not None:
            response = requests.get(f'{self.base_url}/news/everything?source={source}')

            result = self.format_news(response, result)
        else:
            response = requests.get(f'{self.base_url}/news/everything')

            result = self.format_news(response, result)

        return result

    def get_news_source(self):
        news = requests.get(f'{self.base_url}/news/sources')

        return news

    def format_news(self, response, result):
        news_json = response.json()
        news = DotMap(news_json)

        if response:
            for article in news.articles:
                if article.urlToImage and article.urlToImage != 'null':
                    result.append(
                        {
                            'title': article.title,
                            'img': article.urlToImage,
                            'url': article.url,
                        }
                    )
                else:
                    result.append(
                        {
                            'title': article.title,
                            'img': 'https://www.bag.admin.ch/bag/de/home/das-bag/aktuell/news/news-02-09-2020'
                            '/_jcr_content/image.imagespooler.png/1603898250046/588.1000/Icons-18.png',
                            'url': article.url,
                        }
                    )

        return result
