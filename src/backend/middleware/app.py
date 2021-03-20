from flask import Flask
from flask_cors import CORS, cross_origin
from src.routes import api


# Create flask and app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'ASWE_KEY'
api.init_app(app)

CORS(app)


if __name__ == '__main__':
    app.run(port=5600, host='0.0.0.0')
