# Imports.
from flask_restful import Api
from flask import Flask

# Import resources.
from src.resources.current_weather import CurrentWeather
from src.resources.forecast import Forecast

# Create app and api.
app = Flask(__name__)
api = Api(app, prefix="/rest/api/v1")

# Add routes.
api.add_resource(CurrentWeather, "/current-weather")
api.add_resource(Forecast, "/forecast")

# Start server.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5570")
