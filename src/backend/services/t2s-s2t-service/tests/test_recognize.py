# Imports.
from io import BytesIO
import json

# Import setup and teardown.
from tests.BaseCase import BaseCase


class RecognizeTest(BaseCase):
    def test_get_recognize_success(self):
        # Arrange
        message = 'To transfer speech to text use POST /rest/api/v1/recognize.'

        # Act
        response = self.app.get('/rest/api/v1/recognize')

        # Assert
        self.assertEqual(message, response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_post_recognize_success(self):
        # Arrange
        with open('docs/Postman/wetter.weba', 'rb') as audio_file:
            payload = BytesIO(audio_file.read())

        # Act
        response = self.app.post(
            'rest/api/v1/recognize',
            headers={'Content-Type': 'multipart/form-data'},
            data={'audio': (payload, 'wetter.wav')},
        )

        # Assert
        self.assertEqual(
            response.json, {'text': 'how is the weather in Stuttgart '},
        )
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_recognize_no_audio_failure(self):
        # Arrange
        with open('docs/Postman/wetter.weba', 'rb') as audio_file:
            payload = BytesIO(audio_file.read()[14:])

        # Act
        response = self.app.post(
            'rest/api/v1/recognize',
            headers={'Content-Type': 'multipart/form-data'},
            data={'audio': (payload, 'wetter.weba')},
        )

        # Assert
        self.assertEqual(response.status_code, 500)
