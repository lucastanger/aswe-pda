# Imports.
from flask_restful import Resource, reqparse
from ibm_watson import ApiException
from werkzeug import datastructures


class Recognize(Resource):
    '''
        Includes post method. Receives audio file. Returns text.
    '''

    def __init__(self, **kwargs):
        self.ibm = kwargs['ibm']

    def get(self):
        return {"message": "To transfer speech to text use POST /rest/api/v1/recognize."}

    def post(self):
        # Extract audio file from body. Save it as Filestorage.
        parser = reqparse.RequestParser()
        parser.add_argument(
            'audio', required=True, type=datastructures.FileStorage, location='files')
        args = parser.parse_args(strict=True)
        audio_file = args['audio']

        # Recognize.
        try:
            # Recognize speech to text
            speech_recognition_results = self.ibm.speech_to_text.recognize(
                        audio=audio_file.read(),
                        content_type='audio/wav',
                        model='de-DE_BroadbandModel',
                    ).get_result()
            audio_file.close()
        except ApiException as ex:
            # Raise exception if HTTP response code is in the 4xx and 5xx range
            response = {"info": "Error caused by internal service", "error": {
                "code": ex.code, "message": ex.message}}
            return response, 500

        # Extract text from json and return response.
        response = {"text": ""}
        for result in speech_recognition_results["results"]:
            for alternative in result['alternatives']:
                response["text"] += alternative['transcript']

        return response, 200
