# Imports.
from flask_swagger_ui import get_swaggerui_blueprint
from flask_script import Manager, Server
from flask_restful import Api
from yaml import Loader, load
from flask import Flask

# Include setup scripts.
from src.common.setup import Setup

# Import resources.
from src.resources.synthesize import Synthesize
from src.resources.recognize import Recognize


class Ibm():
    '''
        Ibm class. Used to have global variables.
    '''

    def __init__(self):
        self.text_to_speech = None
        self.speech_to_text = None


class CustomServer(Server):
    '''
        CustomServer class. Used to run setup after server startup and before the first request.
    '''

    def __call__(self, app, *args, **kwargs):
        global ibm
        Setup.loadEnv()
        ibm = Setup.authenticate(ibm)
        ibm = Setup.setSettings(ibm)
        kwargs['port'] = 5555
        kwargs['host'] = '0.0.0.0'
        return Server.__call__(self, app, *args, **kwargs)


# Create app, api and manager
app = Flask(__name__)
api = Api(app,
          prefix='/rest/api/v1'
          )
manager = Manager(app)

# Swagger.
SWAGGER_URL = '/rest/api/v1/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = './docs/swagger.yml'  # Our API url (can of course be a local resource)
swagger_yml = load(open(API_URL, 'r'), Loader=Loader)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={
        'app_name': "T2S/S2T-Service",
        'spec': swagger_yml
    },
)
app.register_blueprint(swaggerui_blueprint)

# Create global Ibm object so that every route has access to the variables.
ibm = Ibm()

# Add routes.
api.add_resource(Synthesize, '/synthesize', resource_class_kwargs={'ibm': ibm})
api.add_resource(Recognize, '/recognize', resource_class_kwargs={'ibm': ibm})

# Create custom command.
manager.add_command('runserver', CustomServer())

# Start server.
if __name__ == '__main__':
    manager.run()
