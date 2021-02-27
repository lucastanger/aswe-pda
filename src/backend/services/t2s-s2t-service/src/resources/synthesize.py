# Imports.
from flask_restful import Resource, reqparse
from ibm_watson import ApiException
from flask import send_file
from pathlib import Path
import wave

# Import resources.
from src.common.auth import Auth


class Synthesize(Resource):
    """
    Includes POST and GET methods for synthesize.
    GET Returns information about POST synthesize.
    POST Receives text in json. Returns audio file.
    """

    def __init__(self):
        """
        Authenticate for text to speech.
        """

        self.text_to_speech = Auth.authenticate_t2s(self)

    def get(self):
        """
        Return information about synthesize.
        """

        return {
            'message': 'To transfer text to speech use POST /rest/api/v1/synthesize.'
        }

    def post(self):
        """
        Transfor text to speech.
        Requires text as json in request body.
        Returns audio file.
        """

        # Extract text from request body.
        parser = reqparse.RequestParser()
        parser.add_argument('text', required=True, location='json')
        args = parser.parse_args(strict=True)
        text = args['text']

        # Create static audio folder if not exists.
        Path('./static/audio').mkdir(parents=True, exist_ok=True)

        # Create audio file.
        audio_file = wave.open('static/audio/text2speech.wav', 'wb')
        audio_file.setparams((1, 2, 22050, 0, 'NONE', 'Uncompressed'))

        # Synthesize.
        try:
            audio_file.writeframes(
                # Synthesize text to speech.
                self.text_to_speech.synthesize(
                    text, voice="en-GB_JamesV3Voice", accept="audio/wav"
                )
                .get_result()
                .content
            )
        except ApiException as ex:
            # Raise exception if HTTP response code is in the 4xx and 5xx range.
            response = {
                'info': 'Error caused by internal service',
                'error': {'code': ex.code, 'message': ex.message},
            }
            return response, 500
        finally:
            # Close audio file
            audio_file.close()

        # Create response.
        return send_file(
            'static/audio/text2speech.wav',
            mimetype='audio/wav',
            as_attachment=True,
            attachment_filename='text2speech.wav',
        )
