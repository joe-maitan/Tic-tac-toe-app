from flask import request, render_template
from flask_login import login_required
from config import app, login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash

import unittest
from tests import *

active_users = []

class User():

    def __init__(self, is_authenticated, user_id):
        self._id = user_id
        self._is_authenticated = is_authenticated
        self._is_active = True
        self._is_anonymous = False

    @property
    def is_authenticated(self):
        return self._is_authenticated
    

    @property
    def is_active(self):
        return self._is_active
    

    @property
    def is_anonymous(self):
        return self._is_anonymous


    def get_id(self):
        return self._id


@login_manager.user_loader
def load_user(user_id):
    return db['users'].find_one({"_id": user_id})


# CONVETION: AVOID VERBS IN THE ROUTES
# PLURAL NOUNS ARE PREFFERED
# USE DIFFERENT METHODS TO INDICATE WHAT THE ACTION IS DOING

# @app.route('/heartbeat', methods=["GET"])
# def hearbeat():  # greet the user at the index
#     active_users.append(flask_login.current_user.get_id())
#     app.logger.info("client has joined. Index route was hit")
#     # render_template("index.html")
#     pass


@app.route("/signup", methods=["POST"])
def create_user():
    app.logger.info("/signup route was hit, creating a new user")

    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username:
            app.logger.error("create_user() - Missing username")
            return {"error": "Missing username"}, 400
        
        if not email:
            app.logger.error("create_user() - Missing email")
            return {"error": "Missing email"}, 400
        
        if not password:
            app.logger.error("create_user() - Missing password")
            return {"error": "Missing password"}, 400
        
        existing_email = db['users'].find_one({"email": email})
        existing_username = db['users'].find_one({"username": username})

        if existing_email: 
            return {"error": "Email is already in use."}, 400
              
        if existing_username:
            return {"error": "Username already exists."}, 400 
        
        # hashed_password = generate_password_hash(password) # hash the password
        hashed_password = password

        newUser = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        try:
            db['users'].insert_one(newUser)
            app.logger.info("create_user() - User created and added to database successfully")
        except Exception as e:
            app.logger.error(f"create_user() - Error inserting user into database - {e}")
            return {"error": "Bad request"}, 400

        user = User(True, newUser['username'])

        login_user(user)
           
        return {"message": "User created successfully"}, 201 # This is the status code for created, on the frontend we should redirect them to the lobby
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return {"error": "Internal server error"}, 500
    


@app.route('/login', methods=["POST"])
def login_user():
    app.logger.info("/login route was hit, logging in a user")

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        searched_username = db.users.find_one({"username": username})

        if not searched_username:
            return {"error": "User not found"}, 404
        
        if searched_username.get("password") != password:
            return {"error": "Invalid password"}, 400
        
        user = User(True, searched_username["username"])
        login_user(user)

        app.logger.info("login_user() - User logged in successfully")
        # TODO: redirect them to the game/lobby page
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


@app.route('/logout', methods=["GET"])
@login_required  # an action that requires the user to be logged in
def logout_user():
    app.logger.info("/logout route was hit, logging out a user")
    pass

    # TODO: After logout, take them back to the login page


# TODO: Figure out custom route name for invite, gamemove, etc.
@app.route("/invite", methods=["POST"])
def invite_user():
    app.logger.info("/invite_user route was hit, inviting a user to play a game")
    pass


# @app.route('/play_game') with another user

# @app.route('/play_game_with_bot')


if __name__ == "__main__":
    app.run(debug=True)  # Run all of different routes and our API