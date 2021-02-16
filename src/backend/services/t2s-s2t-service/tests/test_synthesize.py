import unittest
import json

from server import app

class SynthesizeTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_successful_synthesize_get(self):
        # Given
        message = 'To transfer text to speech use POST /rest/api/v1/synthesize.'

        # When
        response = self.app.get('/rest/api/v1/synthesize')

        # Then
        self.assertEqual(message, response.json['message'])
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        pass