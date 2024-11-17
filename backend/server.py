import sys
import socket
import uuid

from flask import request, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room, rooms
from config import socketio, app, login_manager, db
import game

from User import *

#from werkzeug.security import generate_password_hash, check_password_hash

active_user_sockets = {}  # dictionary of active users {user_id: "socket_id"}
active_users = []  # list of active user objects
games = {}

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


def generateGameID() -> str:
    return str(uuid.uuid4())


@login_manager.user_loader
def load_user(user_id: str) -> User:
    # return User.get(user_id)
    user_data = db['users'].find_one({"username": user_id})

    if user_data:
        print(f"load_user() - User {user_data['username']} loaded successfully")
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


@app.route('/logout', methods=["POST"])
def logout() -> jsonify:
    app.logger.info("/logout route was hit, logging out a user")
    
    try:        
        data = request.get_json()

        username = data.get("user_id")
        user = load_user(username)

        if user in active_users:
            active_users.remove(user)
        
        if user in active_user_sockets:
            active_user_sockets.pop(user.get_id())

        return jsonify({"message": f"{user.get_id()} logged out successfully"}), 200
    except Exception as e:
        app.logger.error(f"logout_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400
       


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
    print(f"Active Users: {active_user_sockets}")

    
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

    if (response == "accepted"):
        game_id = generateGameID()
        print(f"Game ID for {inviter} and {invitee}: {game_id}")
        socketio.emit('handle_invite_response', {"invitee": invitee, "inviter": inviter, "response": response, "game_id": game_id})
    else:
        socketio.emit('handle_invite_response', {"invitee": invitee, "inviter": inviter, "response": response})
    

@socketio.on('create_game')
def create_a_game(data):
    print(f"server.py - create_a_game() - event hit")
    print(f"{data}")

    game_id = data.get('game_id')
    
    player1_socketID = active_user_sockets[data.get('player1')]
    player2_socketID = active_user_sockets[data.get('player2')]

    player1 = {
        "username": data.get('player1'),
        "socketID": player1_socketID
    } 

    player2 = {
        "username": data.get('player2'),
        "socketID": player2_socketID
    } 

    if game_id not in games:
        print(f"Inside of if statement")
        games[game_id] = game.Game(game_id, player1, player2)
        # print(f"{games[game_id].board}")

    socketio.emit("game_created", {"game_id": game_id}, to=player1_socketID)
    socketio.emit("game_created", {"game_id": game_id}, to=player2_socketID)


@socketio.on('join_game')
def join_a_game(data):
    game_id = data.get('gameId')
    username = data.get('user')
    join_room(game_id)
    print(f"{username} has joined game room with an id of {game_id}")
    emit('load_board', {'board': games[game_id].get_game_board(), 'user' : username}, to=game_id)


@socketio.on('make_move')
def make_a_move(data):
    game_id = data.get('game_id')

    player_socket_id = active_user_sockets[data.get('player')]
    if games[game_id].get_current_turn() == player_socket_id:
        index = data.get('index')
        player_name = data.get('player')
        print(f"{player_name} is making a move")
        game_state = games[game_id].make_move(player_name, index)

        if game_state == 'True':
            emit('move_made', { 'index': index, 'player': player_name, 'game_state': 'True', 'player_symbol': games[game_id].get_player_symbol(player_name) }, to=game_id)
        elif game_state == 'Draw':
            emit('move_made', { 'index': index, 'player': player_name, 'game_state': 'Draw', 'player_symbol': games[game_id].get_player_symbol(player_name)}, to=game_id)
        else:
            emit('move_made', { 'index': index, 'player': player_name, 'game_state': 'False', 'player_symbol': games[game_id].get_player_symbol(player_name)}, to=game_id)

        games[game_id].switch_turn()
    else:
        print(f"It is not {data.get('player')}'s turn")


@socketio.on('new_game')
def play_again(data):
    game_id = data['game_id']
    games[game_id] = game.Game()


if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname()) # "0.0.0.0"

    if "-p" in sys.argv:
        port_number = int(sys.argv[sys.argv.index("-p") + 1])
    else:
        port_number = 5000

    updateEnvFile(ip_address, port_number)

    socketio.run(app, host=ip_address, port=port_number, debug=True)  # Run all of different routes and our API