# Imports.
import unittest
import json

# Import setup and teardown.
from tests.BaseCase import BaseCase


class SynthesizeTest(BaseCase):
    def test_get_synthesize_success(self):
        # Arrange
        message = 'To transfer text to speech use POST /rest/api/v1/synthesize.'

        # Act
        response = self.app.get('/rest/api/v1/synthesize')

        # Assert
        self.assertEqual(response.json['message'], message)
        self.assertEqual(response.status_code, 200)

    def test_post_synthesize_success(self):
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

    def test_post_synthesize_no_text_failure(self):
        # Arrange
        payload = json.dumps({'text': ''})
        code = 400
        error = 'No text given.'

        # Act
        response = self.app.post(
            'rest/api/v1/synthesize',
            headers={'Content-Type': 'application/json'},
            data=payload,
        )

        # Assert
        self.assertEqual(response.json['error'], error)
        self.assertEqual(response.status_code, code)