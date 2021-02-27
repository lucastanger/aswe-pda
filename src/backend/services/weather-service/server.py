# Imports.
from flask_restful import Api
from flask import Flask

# Import resources.
from src.resources.current_weather import CurrentWeather
from src.resources.forecast import Forecast
from src.common.swagger import Swagger

# Create app and api.
app = Flask(__name__)
api = Api(app, prefix='/rest/api/v1')

# Add swagger to service.
swagger = Swagger()
app.register_blueprint(swagger.connect_swagger())

# Add routes.
api.add_resource(CurrentWeather, '/current-weather')
api.add_resource(Forecast, '/forecast')

# Start server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5570')
