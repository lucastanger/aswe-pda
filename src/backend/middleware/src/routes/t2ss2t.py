from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
import requests
import base64

ns = Namespace('t2ss2t', description='Text to Speech and Speech to Text API')


@ns.route('/synthesize')
class SynthesizeService(Resource):
    def post(self):
        response = requests.post(
            'http://t2s-s2t-service:5555/rest/api/v1/synthesize',
            json={'text': request.json['text']},
        )

        return make_response(
            jsonify({'audio': str(base64.b64encode(response.content).decode('utf-8'))}),
            200,
        )


@ns.route('/recognize')
class RecognizeService(Resource):
    def post(self):
        wav_file = open('text2speech.wav', 'wb')
        decode_string = base64.b64decode(request.json['audio'][22:])
        wav_file.write(decode_string)
        wav_file.close()
        files = {'audio': ('audio.wav', open('text2speech.wav', 'rb'))}

        response = requests.post(
            'http://t2s-s2t-service:5555/rest/api/v1/recognize', files=files,
        )

        print(response)
        print(response.json())
        print(response.text)

        return make_response(response.json(), 200,)
