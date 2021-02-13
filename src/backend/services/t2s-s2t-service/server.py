# Imports.
from flask_script import Manager, Server
from flask_restful import Api
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
        return Server.__call__(self, app, *args, **kwargs)


# Create app, api and manager
app = Flask(__name__)
api = Api(app,
          prefix='/rest/api/v1'
          )
manager = Manager(app)

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
