from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from dotenv import load_dotenv
from os import getenv


class Auth:
    """
    Used to authenticate to IBM CLoud.
    """

    def authenticate_t2s(self):
        """
        Authenticate text to speech API.
        """

        # Load environment variables for t2s
        load_dotenv("ibm-credentials-t2s.env")

        # Authenticate to the API by using IBM Cloud Identity and Access Management (IAM)
        authenticator = IAMAuthenticator(getenv("TEXT_TO_SPEECH_APIKEY"))
        text_to_speech = TextToSpeechV1(authenticator=authenticator)

        # Identify the base URL for the service instance
        text_to_speech.set_service_url(getenv("TEXT_TO_SPEECH_URL"))

        # Disable logging of requests and results
        text_to_speech.set_default_headers({"x-watson-learning-opt-out": "true"})

        return text_to_speech

    def authenticate_s2t(self):
        """
        Authenticate speech to text API.
        """

        # Load environment variables for s2t
        load_dotenv("ibm-credentials-s2t.env")

        # Authenticate to the API by using IBM Cloud Identity and Access Management (IAM)
        authenticator = IAMAuthenticator(getenv("SPEECH_TO_TEXT_APIKEY"))
        speech_to_text = SpeechToTextV1(authenticator=authenticator)

        # Identify the base URL for the service instance
        speech_to_text.set_service_url(getenv("SPEECH_TO_TEXT_URL"))

        # Disable logging of requests and results
        speech_to_text.set_default_headers({"x-watson-learning-opt-out": "true"})

        return speech_to_text
