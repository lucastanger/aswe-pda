import unittest
import json

from server import app

class RecognizeTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_successful_recognize_get(self):
        # Given
        message = 'To transfer speech to text use POST /rest/api/v1/recognize.'

        # When
        response = self.app.get('/rest/api/v1/recognize')

        # Then
        self.assertEqual(message, response.json['message'])
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        pass