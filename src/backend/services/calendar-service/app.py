from flask import Flask

from src.events import events_api

# Create flask and app
app = Flask(__name__)

# Create routes
app.register_blueprint(events_api, url_prefix="/rest/api/v1/events")


if __name__ == "__main__":
    app.run(port=5560, host="0.0.0.0")
