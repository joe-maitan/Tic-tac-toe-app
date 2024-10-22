from flask import request
from config import app, db

# CONVETION: AVOID VERBS IN THE ROUTES
# PLURAL NOUNS ARE PREFFERED
# USE DIFFERENT METHODS TO INDICATE WHAT THE ACTION IS DOING

# @app.route('/)
# greet the user


@app.route('/signup', methods=["GET"])
def create_user():
    # creates a user object with a username, email, and password. This is how they will be identified in the system
    pass


@app.route('/login', methods=["POST"])
def login_user():
    # logs in a user assumming the input username and password match with a username and password
    pass


@app.route('/logout', methods=["GET"])
def logout_user():
    # logs out a user
    pass


@app.route("/invite_user", methods=["POST"])
def invite_user():
    # invites a user to play a game
    pass


# @app.route('/play_game') with another user

# @app.route('/play_game_with_bot')