# Imports.
from flask_restful import Resource, reqparse
from ibm_watson import ApiException
from werkzeug import datastructures

# Import resources.
from src.common.auth import Auth


class Recognize(Resource):
    """
    Includes POST and GET methods for recognize.
    GET Returns information about POST recognize.
    POST Receives audio file. Returns text in json.
    """

    def __init__(self):
        """
        Authenticate for speech to text.
        """

        self.speech_to_text = Auth.authenticate_s2t(self)

    def get(self):
        """
        Return information about recognize.
        """

        return {
            'message': 'To transfer speech to text use POST /rest/api/v1/recognize.'
        }

    def post(self):
        """
        Transfor speech to text.
        Requires audio file.
        Returns text in json.
        """

        # Extract audio file from body. Save it as Filestorage.
        parser = reqparse.RequestParser()
        parser.add_argument(
            'audio', required=True, type=datastructures.FileStorage, location='files'
        )
        args = parser.parse_args(strict=True)
        audio_file = args['audio']

        # Recognize.
        try:
            # Recognize speech to text
            speech_recognition_results = self.speech_to_text.recognize(
                audio=audio_file.read(),
                content_type='audio/webm',
                model='en-US_BroadbandModel',
            ).get_result()
        except ApiException as ex:
            # Raise exception if HTTP response code is in the 4xx and 5xx range
            response = {
                'info': 'Error caused by internal service',
                'error': {'code': ex.code, 'message': ex.message},
            }
            return response, 500
        finally:
            # Close audio file
            audio_file.close()

        # Extract text from json and return response.
        response = {'text': ''}
        for result in speech_recognition_results['results']:
            for alternative in result['alternatives']:
                response['text'] += alternative['transcript']

        return response, 200
