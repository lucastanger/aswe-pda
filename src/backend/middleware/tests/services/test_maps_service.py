from unittest import mock

import pytest
from src.services.maps_service import MapsService

BASE_URL = 'http://maps-service:5580/rest/api/v1'


@pytest.fixture
def service(parameters):
    maps_service = MapsService(parameters)
    return maps_service


class TestCalendarService:
    __origin = 'Stuttgart'
    __destination = 'Berlin'
    __arrival_time = ''

    @mock.patch('requests.get')
    @pytest.mark.parametrize(
        'parameters',
        [
            {
                'origin': __origin,
                'destination': __destination,
                'arrival_time': __arrival_time,
            }
        ],
    )
    def test_query_route_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(
            f'{BASE_URL}/maps/route?origin={self.__origin}&'
            f'destination={self.__destination}&'
            f'arrival_time={self.__arrival_time}'
        )
