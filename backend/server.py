import sys
import socket

from flask import request, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room
from config import socketio, app, login_manager, db

from User import *

#from werkzeug.security import generate_password_hash, check_password_hash

active_user_sockets = {}  # dictionary of active users {user object: "socket_id"}
active_users = []  # list of active user objects


def updateEnvFile(host: str, port: str) -> None:
    with open('../frontend/.env', 'w') as env_file:
        env_file.write(f"VITE_FLASK_HOST={host}\n")
        env_file.write(f"VITE_FLASK_SERVER_PORT={port}\n")


def addUserToActiveUsers(user: User) -> None:
    if user not in active_users:
        active_users.append(user)
    else:
        print(f"User {user.get_id()} is already in the active users list.")


def addUserToActiveUserSockets(user: User, socket_id: str) -> None:
    if user not in active_user_sockets:
        active_user_sockets[user.get_id()] = socket_id
    else:
        print(f"User {user.get_id()} is already in the active user sockets list.")


@login_manager.user_loader
def load_user(user_id: str) -> User:
    # return User.get(user_id)
    user_data = db['users'].find_one({"username": user_id})

    if user_data:
        # print(f"load_user() - User {user_data['username']} loaded successfully")
        return User(is_authenticated=True, user_id=user_data["username"])

    return None


@app.route("/")
def hello_world() -> jsonify:
    app.logger.info("Index route was hit")
    return jsonify({"message": "Hello, World!"}), 200


@app.route("/signup", methods=["POST"])
def create_user() -> jsonify:
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
            addUserToActiveUsers(user)
            app.logger.info("create_user() - User created and added to database successfully")
            return jsonify({"message": "User created successfully"}), 201 # This is the status code for created
        except Exception as e:
            app.logger.error(f"create_user() - Error inserting user into database - {e}")
            return jsonify({"error": "Bad request"}), 400
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return jsonify({"error": "Internal server error"}), 500
    

@app.route('/login', methods=["POST"])
def login() -> jsonify:
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
        addUserToActiveUsers(user)
        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": f"{user.get_id()} logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


@app.route('/logout', methods=["GET"])
@login_required
def logout() -> jsonify:
    app.logger.info("/logout route was hit, logging out a user")
    active_users.remove(current_user)
    logout_user()  # logs out the current user on the page
    pass


@app.route('/profile', methods=["GET"])
@login_required
def profile() -> jsonify:
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        return jsonify({"user_id": user_id, "is_authenticated": current_user.is_authenticated}), 200
    else:
        return jsonify({"error": "User not authenticated"}), 401


@app.route('/active_users', methods=["GET"])
def update_user_list() -> jsonify:
    if not active_users:  # Check if active_users is populated
        app.logger.error("Error: No active users found.")
        return jsonify({"error": "No active users"}), 500

    app.logger.info("/active_users route was hit, updating the list of active users")
    # print(f"Active Users: {[user.get_id() for user in active_users]}")  # Debugging line

    return jsonify({"active_users": [user.get_id() for user in active_users]}), 200
    

@socketio.on('register_user')
def handle_registration(data):
    print(f"handle_connection - event register_user hit - {data}")
    # addUserToActiveUsers(load_user(data.get('userID')))
    addUserToActiveUserSockets(load_user(data.get('userID')), request.sid)
    print(f"{data.get('userID')} has connected to the server")

    
@socketio.on('disconnect')
def handle_disconnect():
    pass


@socketio.on('send_invite')
def handle_send_invite(data):  # send the invite to the invitee
    print(f"server.py - handle_send_invite() - event hit")
    print(f"{data}")

    inviter = load_user(data.get('inviter'))
    invitee = load_user(data.get('invitee'))
    
    # if inviter in active_users and invitee in active_users:  # validate invitee and inviter are active users
    print(f"Inside of if statement: {data.get('inviter')} has invited {data.get('invitee')}")
    invitee_socket_id = active_user_sockets[str(data.get('invitee'))]
    socketio.emit('invite_recieved', {"inviter": data.get('inviter')}, to=invitee_socket_id)


@socketio.on('invite_response')
def handle_respond_invite(data):   # send the response from the invitee back to the inviter
    print(f"server.py - handle_response_invite() - event hit")
    print(f"{data}")

    invitee = data.get('invitee')
    inviter = data.get('inviter')
    response = data.get('response')

    print(f"{invitee} has {response} {inviter}'s invite")
    socketio.emit('handle_invite_response', {"invitee": invitee, "inviter": inviter, "response": response})
    pass


if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname()) # "0.0.0.0"
    port_number = int(sys.argv[1]) if len(sys.argv) > 1 else 5000  # if no port is specified, default to port 5000

    updateEnvFile(ip_address, port_number)

    socketio.run(app, host=ip_address, port=port_number, debug=True)  # Run all of different routes and our API