class NewsService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://news-service:5575/rest/api/v1'

    def query(self):
        return
