# Imports.
from flask_restful import Api
from flask import Flask

# Import resources.
from src.resources.synthesize import Synthesize
from src.resources.recognize import Recognize
from src.common.swagger import Swagger

# Create app and api.
app = Flask(__name__)
api = Api(app, prefix="/rest/api/v1")

# Add swagger to service.
swagger = Swagger()
app.register_blueprint(swagger.connect_swagger())

# Add routes.
api.add_resource(Synthesize, "/synthesize")
api.add_resource(Recognize, "/recognize")

# Start server.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5555")
