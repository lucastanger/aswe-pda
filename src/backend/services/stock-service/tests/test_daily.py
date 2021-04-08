# Import setup and teardown.
from tests.BaseCase import BaseCase

from unittest import mock
import requests


class DailyTest(BaseCase):
    @mock.patch('requests.get')
    def test_get_daily_success(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            'Meta Data': {
                '1. Information': 'Daily Prices (open, high, low, close) and Volumes',
                '2. Symbol': 'BMBL',
                '3. Last Refreshed': '2021-04-07',
                '4. Output Size': 'Full size',
                '5. Time Zone': 'US/Eastern',
            },
            'Time Series (Daily)': {
                '2021-04-07': {
                    '1. open': '63.6600',
                    '2. high': '64.0800',
                    '3. low': '61.8538',
                    '4. close': '62.8700',
                    '5. volume': '738539',
                },
                '2021-04-06': {
                    '1. open': '63.5200',
                    '2. high': '63.9800',
                    '3. low': '61.6000',
                    '4. close': '63.3300',
                    '5. volume': '803708',
                },
                '2021-04-05': {
                    '1. open': '61.9400',
                    '2. high': '64.7800',
                    '3. low': '61.8650',
                    '4. close': '63.9900',
                    '5. volume': '2150884',
                },
                '2021-04-01': {
                    '1. open': '63.2000',
                    '2. high': '64.4300',
                    '3. low': '60.1200',
                    '4. close': '61.4800',
                    '5. volume': '2678472',
                },
                '2021-03-31': {
                    '1. open': '59.6500',
                    '2. high': '63.0400',
                    '3. low': '59.4200',
                    '4. close': '62.3800',
                    '5. volume': '1364346',
                },
                '2021-03-30': {
                    '1. open': '61.8000',
                    '2. high': '62.0422',
                    '3. low': '59.2500',
                    '4. close': '59.4000',
                    '5. volume': '1009739',
                },
                '2021-03-29': {
                    '1. open': '61.4600',
                    '2. high': '63.9900',
                    '3. low': '60.6500',
                    '4. close': '62.0600',
                    '5. volume': '928639',
                },
                '2021-03-26': {
                    '1. open': '62.0500',
                    '2. high': '63.2900',
                    '3. low': '57.4001',
                    '4. close': '62.6000',
                    '5. volume': '1690797',
                },
                '2021-03-25': {
                    '1. open': '61.8100',
                    '2. high': '62.8200',
                    '3. low': '59.7500',
                    '4. close': '61.7200',
                    '5. volume': '2097731',
                },
                '2021-03-24': {
                    '1. open': '66.0100',
                    '2. high': '66.8011',
                    '3. low': '62.5550',
                    '4. close': '62.6800',
                    '5. volume': '973068',
                },
                '2021-03-23': {
                    '1. open': '68.3400',
                    '2. high': '68.8700',
                    '3. low': '65.2500',
                    '4. close': '65.9400',
                    '5. volume': '942559',
                },
                '2021-03-22': {
                    '1. open': '68.0700',
                    '2. high': '69.4500',
                    '3. low': '66.8900',
                    '4. close': '68.3700',
                    '5. volume': '903416',
                },
                '2021-03-19': {
                    '1. open': '67.5926',
                    '2. high': '69.2300',
                    '3. low': '65.0800',
                    '4. close': '68.1600',
                    '5. volume': '2068537',
                },
                '2021-03-18': {
                    '1. open': '70.2500',
                    '2. high': '71.1800',
                    '3. low': '65.5800',
                    '4. close': '66.1900',
                    '5. volume': '2652648',
                },
                '2021-03-17': {
                    '1. open': '71.0900',
                    '2. high': '72.9200',
                    '3. low': '69.3600',
                    '4. close': '72.6700',
                    '5. volume': '2213614',
                },
                '2021-03-16': {
                    '1. open': '74.0100',
                    '2. high': '74.5800',
                    '3. low': '69.7700',
                    '4. close': '73.0000',
                    '5. volume': '1566015',
                },
                '2021-03-15': {
                    '1. open': '69.4400',
                    '2. high': '74.7999',
                    '3. low': '69.1200',
                    '4. close': '73.4700',
                    '5. volume': '2604648',
                },
                '2021-03-12': {
                    '1. open': '67.6700',
                    '2. high': '72.2000',
                    '3. low': '63.0000',
                    '4. close': '69.2600',
                    '5. volume': '2837383',
                },
                '2021-03-11': {
                    '1. open': '71.1000',
                    '2. high': '76.4900',
                    '3. low': '67.1000',
                    '4. close': '69.7600',
                    '5. volume': '8697648',
                },
                '2021-03-10': {
                    '1. open': '65.3000',
                    '2. high': '65.5000',
                    '3. low': '61.0400',
                    '4. close': '62.9100',
                    '5. volume': '2215068',
                },
                '2021-03-09': {
                    '1. open': '62.4900',
                    '2. high': '63.9300',
                    '3. low': '61.3000',
                    '4. close': '63.3000',
                    '5. volume': '1393064',
                },
                '2021-03-08': {
                    '1. open': '59.4300',
                    '2. high': '63.4700',
                    '3. low': '57.5500',
                    '4. close': '60.5000',
                    '5. volume': '1920677',
                },
                '2021-03-05': {
                    '1. open': '60.6100',
                    '2. high': '62.2900',
                    '3. low': '57.5300',
                    '4. close': '61.6500',
                    '5. volume': '3036761',
                },
                '2021-03-04': {
                    '1. open': '62.0000',
                    '2. high': '64.3500',
                    '3. low': '58.5766',
                    '4. close': '59.6400',
                    '5. volume': '3985582',
                },
                '2021-03-03': {
                    '1. open': '67.5000',
                    '2. high': '68.3542',
                    '3. low': '61.3800',
                    '4. close': '62.0100',
                    '5. volume': '2895983',
                },
                '2021-03-02': {
                    '1. open': '73.0000',
                    '2. high': '73.7603',
                    '3. low': '67.5200',
                    '4. close': '67.8700',
                    '5. volume': '1417249',
                },
                '2021-03-01': {
                    '1. open': '68.5100',
                    '2. high': '74.7500',
                    '3. low': '67.5000',
                    '4. close': '74.5100',
                    '5. volume': '3854090',
                },
                '2021-02-26': {
                    '1. open': '64.6100',
                    '2. high': '70.8800',
                    '3. low': '64.5119',
                    '4. close': '67.3100',
                    '5. volume': '2422532',
                },
                '2021-02-25': {
                    '1. open': '67.5800',
                    '2. high': '70.3299',
                    '3. low': '61.1700',
                    '4. close': '63.9800',
                    '5. volume': '3347111',
                },
                '2021-02-24': {
                    '1. open': '65.5800',
                    '2. high': '70.4400',
                    '3. low': '61.9000',
                    '4. close': '68.5000',
                    '5. volume': '3710894',
                },
                '2021-02-23': {
                    '1. open': '65.0000',
                    '2. high': '66.9900',
                    '3. low': '61.6200',
                    '4. close': '65.4700',
                    '5. volume': '4379795',
                },
                '2021-02-22': {
                    '1. open': '71.0543',
                    '2. high': '72.4400',
                    '3. low': '64.8100',
                    '4. close': '67.2000',
                    '5. volume': '8028371',
                },
                '2021-02-19': {
                    '1. open': '75.0100',
                    '2. high': '75.7000',
                    '3. low': '70.1900',
                    '4. close': '71.7500',
                    '5. volume': '5095535',
                },
                '2021-02-18': {
                    '1. open': '75.4500',
                    '2. high': '76.4000',
                    '3. low': '73.6300',
                    '4. close': '74.0000',
                    '5. volume': '3166412',
                },
                '2021-02-17': {
                    '1. open': '76.7800',
                    '2. high': '78.6977',
                    '3. low': '75.0000',
                    '4. close': '77.3200',
                    '5. volume': '3762128',
                },
                '2021-02-16': {
                    '1. open': '79.1500',
                    '2. high': '79.6000',
                    '3. low': '70.3778',
                    '4. close': '78.8900',
                    '5. volume': '13163020',
                },
                '2021-02-12': {
                    '1. open': '75.7100',
                    '2. high': '84.8000',
                    '3. low': '71.5100',
                    '4. close': '75.4600',
                    '5. volume': '21414245',
                },
                '2021-02-11': {
                    '1. open': '76.0000',
                    '2. high': '79.6000',
                    '3. low': '70.0000',
                    '4. close': '70.3100',
                    '5. volume': '43502658',
                },
            },
        }

        symbol = 'BMBL'
        code = 200

        # Act
        response = self.app.get('/rest/api/v1/daily?symbol={}'.format(symbol))

        # Assert
        self.assertEqual(response.json['Meta Data']['2. Symbol'], symbol)
        self.assertEqual(response.status_code, code)

    @mock.patch('requests.get')
    def test_get_daily_api_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'
        }

        symbol = 'BMBL'
        code = 500
        info = 'Internal server error caused by third party api.'

        # Act
        response = self.app.get('/rest/api/v1/daily?symbol={}'.format(symbol))

        # Assert
        self.assertEqual(response.json['info'], info)
        self.assertEqual(response.status_code, code)

    @mock.patch('requests.get')
    def test_get_daily_no_or_wrong_symbol_failure(self, mocked_get):
        # Arrange
        mocked_get.return_value.json.return_value = {
            'Error Message': 'Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY.'
        }

        symbol = ''
        code = 500
        info = 'Internal server error caused by third party api.'

        # Act
        response = self.app.get('/rest/api/v1/daily?symbol={}'.format(symbol))

        # Assert
        self.assertEqual(response.json['info'], info)
        self.assertEqual(response.status_code, code)
