from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room
from config import socketio, app, login_manager, db

from User import *

#from werkzeug.security import generate_password_hash, check_password_hash

active_users = {}  # dictionary of active users {"username": "socket_id"}


@login_manager.user_loader
def load_user(user_id: str) -> User:
    # return User.get(user_id)
    user_data = db['users'].find_one({"username": user_id})

    if user_data:
        print(f"load_user() - User {user_data['username']} loaded successfully")
        return User(is_authenticated=True, user_id=user_data["username"])

    return None


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
        
        existing_username = db['users'].find_one({"username": username})
        existing_email = db['users'].find_one({"email": email})
        
        if existing_username:
            app.logger.error("create_user() - username already in use for another account")
            return jsonify({"error": "Username already exists. Please choose another."}), 400
        
        if existing_email: 
            app.logger.error("create_user() - email in use for another account")
            return jsonify({"error": "Email already exists. Please choose another."}), 400
              
        # hashed_password = generate_password_hash(password) # hash the password
        hashed_password = password

        newUser = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        try:
            db['users'].insert_one(newUser)
            user = load_user(db['users'].find_one({"username": username})["username"])
            login_user(user, remember=True)

            app.logger.info("create_user() - User created and added to database successfully")
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
        # print(f"{data}")
        username = data.get("username")
        password = data.get("password")

        if not username:
            app.logger.error("login_user() - Missing username")
            return jsonify({"error": "Missing username"}), 400
        
        if not password:
            app.logger.error("login_user() - Missing password")
            return jsonify({"error": "Missing password"}), 400

        searched_username = db['users'].find_one({"username": username})
        if not searched_username:
            app.logger.info("/login username not found in database")
            return {"error": "Username not found"}, 404
        
        if searched_username.get("password") != password:
            return {"error": "Invalid password"}, 400
        
        
        user = load_user(searched_username["username"])
        login_user(user, remember=True)
        print(f"Current user after logig_user in login() - {current_user.get_id()}")
        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": "User logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    app.logger.info("/logout route was hit, logging out a user")
    logout_user()  # logs out the current user on the page
    pass


@app.route('/profile', methods=["GET"])
@login_required
def profile():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        return jsonify({"user_id": user_id, "is_authenticated": current_user.is_authenticated}), 200
    else:
        return jsonify({"error": "User not authenticated"}), 401


@socketio.on('connect')
@login_required
def handle_connection():
    print(f"server.py - handle_connection() - event hit")
    print(f"Current user in handle_connect: {current_user.get_id()}")
    print(f"handle_connection() - session username {session.get('username')}")
    print(f"handle_connection() - session is_authenticated {session.get('is_authenticated')}")
    print(f"server.py - handle_connection() - request.sid = {request.sid}")

    if session.get('is_authenticated'):
        print(f"handle_connection() - current session is {session.get('is_authenticated')}")
        active_users[session.get('username')] = request.sid  # pairs the current user to their socket id


@socketio.on('user_join')
def user_join(username):
    print(f"server.py - handle_connection() - event hit")
    print(f"Current user in handle_connect: {username}")
    print(f"{current_user.get_id()}")
    active_users["username"] = username  # TODO: Figure out how to store active users with their username as the key, and socket id as the value
    print(f"ACTIVE USERS: {active_users}")
    
    # TODO: Only send one broadcast/emit after a user joins
    emit("user_list_update", {"users": active_users}, broadcast=True)
    # active_users[username] = request.sid  # pairs the current user to their socket id
    emit("user_list_update", {"users": list(active_users.keys())}, broadcast=True)
    

@socketio.on('disconnect')
@login_required
def handle_disconnection():
    app.logger.info("A user has disconnected from the server")
    pass


@socketio.on('user_list_update')
@login_required
def update_user_list():
    print(f"update_user_list() - user_list_update event hit")
    pass


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