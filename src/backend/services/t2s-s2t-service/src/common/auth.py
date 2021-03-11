from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
from dotenv import load_dotenv
from os import getenv


class Auth:
    """
    Used to authenticate to IBM CLoud and Google Cloud.
    """

    def loadEnv(self):
        """
        Load environment variables
        """

        # Load environment variables
        load_dotenv('./.secrets/t2s-s2t-service.env')

    def authenticate_s2t(self):
        """
        Authenticate speech to text API and get google credentials.
        """

        Auth.loadEnv(self)

        # Authenticate to the API by using IBM Cloud Identity and Access Management (IAM)
        authenticator = IAMAuthenticator(getenv('SPEECH_TO_TEXT_APIKEY'))
        speech_to_text = SpeechToTextV1(authenticator=authenticator)

        # Identify the base URL for the service instance
        speech_to_text.set_service_url(getenv('SPEECH_TO_TEXT_URL'))

        # Disable logging of requests and results
        speech_to_text.set_default_headers({'x-watson-learning-opt-out': 'true'})

        return speech_to_text
