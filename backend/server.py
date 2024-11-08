from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room
from config import socketio, app, login_manager, db

from User import *

#from werkzeug.security import generate_password_hash, check_password_hash

active_user_sockets = {}  # dictionary of active users {user object: "socket_id"}
active_users = []  # list of active user objects


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
        active_users.append(user)
        print(f"Current user after login_user in login() - {current_user.get_id()}")
        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": f"{user.get_id()} logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    app.logger.info("/logout route was hit, logging out a user")
    active_users.remove(current_user)
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


@app.route('/active_users', methods=["GET"])
def update_user_list():
    if not active_users:  # Check if active_users is populated
        app.logger.error("Error: No active users found.")
        return jsonify({"error": "No active users"}), 500

    app.logger.info("/active_users route was hit, updating the list of active users")
    # print(f"Active Users: {[user.get_id() for user in active_users]}")  # Debugging line

    return jsonify({"active_users": [user.get_id() for user in active_users]}), 200
    

# # socketio.on('register_user')  # this is the same as connecting
# def handle_register_user():
#     print(f"server.py - handle_register_user() - event hit")
#     print(f"Current user in handle_register_user(): {current_user.get_id()}")
#     #new_user = load_user(data["username"])
#     new_user = current_user 

#     if new_user:
#         print(f"handle_register_user() - new user {new_user.get_id()} loaded successfully")
#         # active_users[new_user] = socket_id  # Store the user object with their socket ID
#         active_users.append(new_user)
#         print(active_users)
#         return jsonify({"message": f"User {new_user.get_id()} registered successfully"}), 200
#     else:
#         return jsonify({"error": "User not found"}), 404


@socketio.on('connect_to_backend')
def handle_connect():
    user_id = current_user.get_id()
    active_user_sockets[user_id] = request.sid  # Map user_id to socket ID
    print(f"{user_id} connected.")


@socketio.on('disconnect')
def handle_disconnect():
    user_id = next((user for user, sid in active_user_sockets.items() if sid == request.sid), None)
    if user_id:
        del active_user_sockets[user_id]
        print(f"{user_id} disconnected.")


@socketio.on('send_invite')
def handle_send_invite(data):
    print(f"server.py - handle_send_invite() - event hit")
    print(f"Current user in handle_send_invite(): {current_user.get_id()}")
    inviter = data.get('inviter')
    invitee = data.get('invitee')
    if invitee in active_users:
        # Emit an event to the invitee to notify them of the invitation
        emit('receive_invite', {'inviter': inviter}, room=active_user_sockets[invitee])
        print(f"Invite sent from {inviter} to {invitee}")
    else:
        emit('invite_error', {'error': f"{invitee} is not online"}, room=active_user_sockets[inviter])


@socketio.on('respond_invite')
def handle_respond_invite(data):
    inviter = data.get('inviter')
    invitee = data.get('invitee')
    response = data.get('response')  # 'accepted' or 'declined'
    if inviter in active_users:
        # Notify the inviter of the invitee's response
        emit('invite_response', {'invitee': invitee, 'response': response}, room=active_user_sockets[inviter])
        print(f"{invitee} has {response} the invite from {inviter}")


if __name__ == "__main__":
    # app.run(debug=True)  # Run all of different routes and our API
    socketio.run(app, debug=True)  # Run all of different routes and our API