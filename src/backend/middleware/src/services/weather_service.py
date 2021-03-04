class WeatherService:
    def __init__(self, parameters: dict = None):
        self.parameters = parameters
        self.base_url = 'http://weather-service:5570/rest/api/v1'

    def query(self):
        return
