from flask import Flask

from src.maps import maps_api

# Create flask and app
app = Flask(__name__)

# Create routes
app.register_blueprint(maps_api, url_prefix='/rest/api/v1/maps')


if __name__ == '__main__':
    app.run(port=5580, host='0.0.0.0')
