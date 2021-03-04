from .calendar_service import CalendarService
from .dualis_service import DualisService
from .maps_service import MapsService
from .news_service import NewsService
from .spotify_service import SpotifyService
from .weather_service import WeatherService

calendar_service = CalendarService()
dualis_service = DualisService()
maps_service = MapsService()
news_service = NewsService()
spotify_service = SpotifyService()
weather_service = WeatherService()


def query(intent, parameters):
    switch = {
        'calendar-intent': calendar_service,
        'dualis-intent': dualis_service,
        'maps-intent': maps_service,
        'news-intent': news_service,
        'spotify-intent': spotify_service,
        'weather-intent': weather_service,
    }
    service = switch.get(intent, lambda: 'Unknown intent.')
    service.__init__(parameters)
    return service.query()
