from flask import Flask

from src import api

# Create flask and app
app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':
    app.run(port=5580, host='0.0.0.0')
