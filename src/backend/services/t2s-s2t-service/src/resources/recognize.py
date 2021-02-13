from flask_restful import Resource, reqparse
from werkzeug import datastructures
import wave


class Recognize(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'audio', required=True, type=datastructures.FileStorage, location='files')
        args = parser.parse_args(strict=True)
        print(args['audio'])
        stream = args['audio'].stream

        with wave.open(stream, 'rb') as audio_file:
            print(audio_file.getframerate())

        # wav_file = wave.open(stream, 'rb')
        # fs = wav_file.getframerate()
        # wav_file.close()

        # print(stream)
        # print(fs)
        # print(wav_file)
