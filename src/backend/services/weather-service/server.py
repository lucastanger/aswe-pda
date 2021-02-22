# Imports.
from flask_restful import Api
from flask import Flask

# Create app and api.
app = Flask(__name__)
api = Api(app, prefix="/rest/api/v1")

# Start server.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5570")
