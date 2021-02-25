# Imports.
import unittest
import json

# Import setup and teardown.
from tests.BaseCase import BaseCase


class SynthesizeTest(BaseCase):
    def test_successful_synthesize_get(self):
        # Arrange
        message = 'To transfer text to speech use POST /rest/api/v1/synthesize.'

        # Act
        response = self.app.get('/rest/api/v1/synthesize')

        # Assert
        self.assertEqual(response.json['message'], message)
        self.assertEqual(response.status_code, 200)

    def test_successful_synthesize_post(self):
        # Arrange
        payload = json.dumps({'text': 'Test'})

        # Act
        response = self.app.post(
            'rest/api/v1/synthesize',
            headers={'Content-Type': 'application/json'},
            data=payload,
        )

        # Assert
        self.assertEqual(
            response.headers['Content-Disposition'],
            'attachment; filename=text2speech.wav',
        )
        self.assertEqual(response.headers['Content-Type'], 'audio/wav')
        self.assertEqual(response.status_code, 200)
