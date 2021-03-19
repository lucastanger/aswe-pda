# Imports.
from flask_restful import Api
from flask import Flask

# Import resources.
from src.resources.symbol import Symbol
from src.resources.daily import Daily
from src.resources.today import Today
from src.common.swagger import Swagger

# Create app and api.
app = Flask(__name__)
api = Api(app, prefix='/rest/api/v1')

# Add swagger to service.
swagger = Swagger()
app.register_blueprint(swagger.connect_swagger())

# Add routes.
api.add_resource(Symbol, '/symbol')
api.add_resource(Daily, '/daily')
api.add_resource(Today, '/today')

# Start server.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5585')
