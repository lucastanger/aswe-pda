from flask import Flask, redirect, request, session, g, render_template
import flask_spotify_auth, profile

app = Flask(__name__)
app.secret_key = "some key for session"


@app.route("/")
def home():
    return "Spotify Service"


@app.route("/auth")
def auth():
    return redirect(flask_spotify_auth.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args["code"]
    auth_header = flask_spotify_auth.authorize(auth_token)
    session["auth_header"] = auth_header

    return prof()


def valid_token(resp):
    return resp is not None and not "error" in resp


@app.route("/profile")
def prof():
    if "auth_header" in session:
        auth_header = session["auth_header"]

        profile_data = profile.getUserProfile(auth_header)

        playlist_data = profile.getUserPlaylists(auth_header)

        recently_played = profile.getUserRecentlyPlayed(auth_header)

        if valid_token(recently_played):
            return "Profildaten gefunden!"


if __name__ == "__main__":
    app.run(port=5565, host="0.0.0.0")
