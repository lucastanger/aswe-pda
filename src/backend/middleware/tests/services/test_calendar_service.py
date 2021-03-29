import datetime
from unittest import mock

import pytest
import pytz
from src.services.calendar_service import CalendarService

BASE_URL = 'http://calendar-service:5560/rest/api/v1'


@pytest.fixture
def service(parameters):
    calendar_service = CalendarService(parameters)
    return calendar_service


class TestCalendarService:
    __date = '2021-03-26T12:00:00+01:00'

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'date': __date, 'calendar-alarm': ''}])
    def test_query_date_success(self, mocked_get, service):
        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/events/{self.__date}')

    @mock.patch('requests.get')
    @pytest.mark.parametrize('parameters', [{'date': '', 'calendar-alarm': 'alarm'}])
    def test_query_alarm_success(self, mocked_get, service):
        date_tomorrow = (
            (
                datetime.datetime.utcnow().astimezone(pytz.timezone('Europe/Berlin'))
                + datetime.timedelta(days=1)
            )
            .replace(hour=0, minute=0, second=0)
            .strftime('%Y-%m-%dT%H:%M:%S%z')
        )

        _response = service.query()

        mocked_get.assert_called_with(f'{BASE_URL}/events/{date_tomorrow}')
