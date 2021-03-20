# Imports.
from flask_restful import Resource, reqparse
from google.cloud import texttospeech
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

        Auth.loadEnv(self)

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

        # Only accept if text is not empty
        if not text:
            response_error = {'error': 'No text given.'}
            return response_error, 400

        # Create static audio folder if not exists.
        Path('./static/audio').mkdir(parents=True, exist_ok=True)

        # Create audio file.
        audio_file = wave.open('static/audio/text2speech.wav', 'wb')
        audio_file.setparams((1, 2, 22050, 0, 'NONE', 'Uncompressed'))

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-GB',
            name='en-GB-Wavenet-B',
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open('static/audio/text2speech.wav', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)

        # Create response.
        return send_file(
            'static/audio/text2speech.wav',
            mimetype='audio/wav',
            as_attachment=True,
            attachment_filename='text2speech.wav',
        )
