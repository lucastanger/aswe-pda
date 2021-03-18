from flask_swagger_ui import get_swaggerui_blueprint
from yaml import Loader, load


class Swagger:
    """
    Class to create and connect to static Swagger yml file.
    """

    def __init__(self):
        """
        Set base url and load static yml file.
        """

        self.SWAGGER_URL = (
            '/rest/api/v1/docs'  # URL for exposing Swagger UI (without trailing '/')
        )
        self.API_URL = (
            './docs/swagger.yml'  # Our API url (can of course be a local resource)
        )
        self.swagger_yml = load(open(self.API_URL, 'r'), Loader=Loader)

    def connect_swagger(self):
        """
        Creates and returns swaggerui blueprint
        """

        # Call factory function to create our blueprint.
        self.swaggerui_blueprint = get_swaggerui_blueprint(
            self.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
            self.API_URL,
            config={'app_name': 'Stock-Service', 'spec': self.swagger_yml},
        )

        return self.swaggerui_blueprint
