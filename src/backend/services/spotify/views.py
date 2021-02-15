from flask import Flask, redirect, request
import startup, flask_spotify_auth

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/auth")
def auth():
    result = startup.getUser()
    return redirect(result)


@app.route("/callback/")
def call():
    #token = request.args['code']
    #user_token = startup.getUserToken(token)
    return f"Der User Token lautet: "

if __name__ == '__main__':
    app.run(port=5565, host="0.0.0.0")