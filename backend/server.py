from flask import Flask, request, session, jsonify, render_template
from flask_cors import CORS
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from config import socketio, app, login_manager, db

#from werkzeug.security import generate_password_hash, check_password_hash

# Constant HTTP status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500

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


def get_user(username):
    return db['users'].find_one({"username": username})


@app.route("/")
def hello_world():
    app.logger.info("Index route was hit")
    return jsonify({"message": "Hello, World!"}), 200


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
            return jsonify({"error": "Missing username"}), 400
        
        if not email:
            app.logger.error("create_user() - Missing email")
            return jsonify({"error": "Missing email"}), 400
        
        if not password:
            app.logger.error("create_user() - Missing password")
            return jsonify({"error": "Missing password"}) , 400
        
        existing_email = db['users'].find_one({"email": email})
        existing_username = db['users'].find_one({"username": username})

        if existing_email: 
            app.logger.error("create_user() - email already in the database")
            return jsonify({"error": "Email is already in use."}), 400
              
        if existing_username:
            app.logger.error("create_user() - username already in the database")
            return jsonify({"error": "Username already exists."}), 400
        
        # hashed_password = generate_password_hash(password) # hash the password
        hashed_password = password

        newUser = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        try:
            app.logger.info("create_user() - User created and added to database successfully")
            db['users'].insert_one(newUser)
            user = User(True, newUser['username'])
            login_user(user)

            # Set session as authenticated
            session['authenticated'] = True
            session['username'] = username  # You can add other user information if needed
            
            return jsonify({"message": "User created successfully"}), 201 # This is the status code for created
        except Exception as e:
            app.logger.error(f"create_user() - Error inserting user into database - {e}")
            return jsonify({"error": "Bad request"}), 400
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return jsonify({"error": "Internal server error"}), 500
    


@app.route('/login', methods=["POST"])
def login():
    app.logger.info("/login route was hit, logging in a user")

    try:
        data = request.get_json()
        # print(data)
        username = data.get("username")
        password = data.get("password")

        searched_username = db['users'].find_one({"username": username})
        if not searched_username:
            app.logger.info("/login username not found in database")
            return {"error": "User not found"}, 404
        
        if searched_username.get("password") != password:
            return {"error": "Invalid password"}, 400
        
        user = User(True, searched_username["username"])
        login_user(user)

        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": "User logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


@login_required  # an action that requires the user to be logged in
@app.route('/logout', methods=["GET"])
def logout():
    app.logger.info("/logout route was hit, logging out a user")
    # how to get the username/id of the user that sent this request
    # logout_user()
    pass

    # TODO: After logout, take them back to the login page


@login_required
@socketio.on('connect')
def handle_connection():
    print("server.py - handle_connection() - user has connected to the server VIA sockets")
    app.logger.info("A user has connected to the server")
    # emit('connect', {"data": current_user.username + " has connected"})
    active_users.append(current_user)
    pass


@login_required
@socketio.on('disconnect')
def handle_disconnection():
    app.logger.info("A user has disconnected from the server")
    # emit('disconnect', {"data": current_user['username'] + " has disconnected"})
    active_users.remove(current_user)
    pass


# @login_required
# @socketio.on('heartbeat')
# def send_heartbeat():
#     app.logger.info("A user has sent a heartbeat")
#     emit('heartbeat', {"data": "Hello, World!"})
#     pass


# TODO: Figure out the socket stuff behind invite, creating the room for two players, and make move
# @login_required
# @socketio.on('invite')
# def invite_user():
#     app.logger.info("/invite_user route was hit, inviting a user to play a game")
#     pass


# @login_required
# @socketio.on('gamemove')
# def game_move(game_board, postion):
#     app.logger.info("/game_move route was hit, making a move in the game")
#     pass


if __name__ == "__main__":
    # app.run(debug=True)  # Run all of different routes and our API
    socketio.run(app, debug=True)  # Run all of different routes and our API