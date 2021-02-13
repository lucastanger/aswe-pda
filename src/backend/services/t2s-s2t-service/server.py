from flask import Flask
from flask_restful import Api
from flask_script import Manager, Server

from src.common.setup import Setup

# Import resources
from src.resources.recognize import Recognize
from src.resources.synthesize import Synthesize
 
# Global variables
speech_to_text = None
text_to_speech = None


class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        Setup.loadEnv()
        Setup.authenticate()
        Setup.setSettings()
        return Server.__call__(self, app, *args, **kwargs)


app = Flask(__name__)
api = Api(app)
manager = Manager(app)

# Add routes
api.add_resource(Recognize, '/recognize')
api.add_resource(Synthesize, '/synthesize')

manager.add_command('runserver', CustomServer())

if __name__ == '__main__':
    manager.run()
