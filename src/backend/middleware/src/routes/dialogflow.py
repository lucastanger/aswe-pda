import json
import os
from os.path import dirname, join

from dotmap import DotMap
from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, reqparse
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow_v2
from google.protobuf.json_format import MessageToDict

from src.services import query

ns = Namespace('dialogflow', description='Dialogflow APIs')

parser = reqparse.RequestParser()
parser.add_argument(
    'message', type=str, help='Message used to detect intent with dialogflow.'
)

with open('docs/dialogflow_response.json') as json_file:
    dialogflow_response = json.load(json_file)


@ns.route('/query')
@ns.response(400, 'Missing argument: message')
@ns.expect(parser)
class Dialogflow(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        project_root = dirname(dirname(dirname(__file__)))
        output_path = join(project_root, '.secrets/dhbw-aswe-pda.json')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = output_path

        self.DIALOGFLOW_PROJECT_ID = 'dhbw-aswe-pda-1613143292614'
        self.DIALOGFLOW_LANGUAGE_CODE = 'en'
        self.LOCATION_ID = 'europe-west1'
        self.SESSION_ID = 'pda'

    @ns.response(200, json.dumps(dialogflow_response, indent=2))
    def post(self):
        parsed_request = DotMap(request.json)
        message = parsed_request.message

        session_client = dialogflow_v2.SessionsClient(
            client_options={
                'api_endpoint': f'{self.LOCATION_ID}-dialogflow.googleapis.com'
            }
        )

        session = (
            f'projects/{self.DIALOGFLOW_PROJECT_ID}/locations/{self.LOCATION_ID}/'
            f'agent/sessions/{self.SESSION_ID}'
        )

        text_input = dialogflow_v2.types.TextInput(
            text=message, language_code=self.DIALOGFLOW_LANGUAGE_CODE
        )
        query_input = dialogflow_v2.types.QueryInput(text=text_input)

        try:
            response = session_client.detect_intent(
                session=session, query_input=query_input
            )
            dict_response = MessageToDict(
                response._pb, preserving_proto_field_name=True
            )
            parsed_response = DotMap(dict_response)
        except InvalidArgument:
            raise

        print('Query text:', parsed_response.query_result.query_text)
        print('Detected intent:', parsed_response.query_result.intent.display_name)
        print(
            'Detected intent confidence:',
            parsed_response.query_result.intent_detection_confidence,
        )
        print('Fulfillment text:', parsed_response.query_result.fulfillment_text)

        # Parse response to audio file
        with open('response.wav', 'wb') as out:
            out.write(response.output_audio)
            print('Audio content written to file "response.wav"')

        # Call the corresponding function for the intent
        parameters = parsed_response.query_result.parameters.toDict()
        service_response = query(
            parsed_response.query_result.intent.display_name, parameters
        )

        return make_response(
            jsonify({'response': service_response, 'dialogflow': dict_response}), 200
        )
