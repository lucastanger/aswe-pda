from flask import Flask

from src.routes import api

# Create flask and app
app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
    app.run(port=5600, host='0.0.0.0')
