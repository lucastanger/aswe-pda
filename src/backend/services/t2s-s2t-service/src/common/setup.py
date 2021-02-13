from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from dotenv import load_dotenv
from os import getenv


class Setup():

    def loadEnv():
        # Load environment variables
        load_dotenv('ibm-credentials-s2t.env')
        load_dotenv('ibm-credentials-t2s.env')

        print("INFO: Environment variables loaded.")

    def authenticate():
        global speech_to_text, text_to_speech

        # Authenticate to the API by using IBM Cloud Identity and Access Management (IAM)
        authenticator = IAMAuthenticator(getenv("SPEECH_TO_TEXT_APIKEY"))
        speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        authenticator = IAMAuthenticator(getenv("TEXT_TO_SPEECH_APIKEY"))
        text_to_speech = TextToSpeechV1(
            authenticator=authenticator
        )

        # Identify the base URL for the service instance
        speech_to_text.set_service_url(getenv("SPEECH_TO_TEXT_URL"))
        text_to_speech.set_service_url(getenv("TEXT_TO_SPEECH_URL"))

        print("INFO: Authenticated to IBM Cloud.")

    def setSettings():
        global speech_to_text, text_to_speech

        # Disable logging of requests and results
        speech_to_text.set_default_headers(
            {'x-watson-learning-opt-out': "true"})
        text_to_speech.set_default_headers(
            {'x-watson-learning-opt-out': "true"})

        print("INFO: Disabled logging.")
