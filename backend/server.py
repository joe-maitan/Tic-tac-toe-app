import sys
import socket
import uuid
import game
import subprocess

from flask import request, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room, rooms
from config import socketio, app, login_manager, db
from User import *


active_user_sockets = {}  # dictionary of active users {user_id: "socket_id"}
active_users = []  # list of active user objects
games = {}


#allows clients to connect to the server that's running on a different machine
def update_env_file(host: str, port: str) -> None:
    with open('../frontend/.env', 'w') as env_file:
        env_file.write(f"VITE_FLASK_HOST={host}\n")
        env_file.write(f"VITE_FLASK_SERVER_PORT={port}\n")

# run_server_tests()
# @param None
# @brief This creates a subprocess that will run all of the unit tests on the backend. 
# This grabs whatever version of python you have and executes the tests
# @return a boolean value depending on if the tests passed or not
def run_server_tests():
    try:
        # result = subprocess.run(
        #     [sys.executable, "-m", "pytest"],
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     text=True
        # )

        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            text=True  # Ensures output is handled as text, not bytes
        )

        print("Test Output:\n", result.stdout)
        if result.returncode == 0:
            print("Tests passed successfully!")
            return True
        else:
            print("Tests failed!")
            return False
    except Exception as e:
        print(f"An error occurred while running tests: {e}")
        return False


#adds new user to active users list when entering lobby
def add_user_to_active_users(user: User) -> None:
    if user not in active_users:
        active_users.append(user)
    else:
        print(f"User {user.get_id()} is already in the active users list.")


#adds new user to active sockets list when entering lobby
def add_user_to_active_users_sockets(user: User, socket_id: str) -> None:
    if user not in active_user_sockets:
        active_user_sockets[user.get_id()] = socket_id
    else:
        print(f"User {user.get_id()} is already in the active user sockets list.")


#handles users disconnecting from the server
def logout_user(user: User) -> None:
    print(f"logout_user() - Current active users list {active_users}")
    for temp_user in active_users:
        if temp_user.get_id() == user.get_id():
            print(f"logout_user() - {user} is being removed from active_users list")
            active_users.remove(temp_user)
            print(f"logout_user() - After removal of the user active users list {active_users}")
            print(f"logout_user() - {user.get_id()} removed from active_users list")

    print(f"logout_user() - Current active user sockets list {active_user_sockets}")
    if user in active_user_sockets:
        print(f"logout_user() - {user.get_id()} removed from active_user_sockets list")
        active_user_sockets.pop(user.get_id())


#generate game ID
def generate_game_ID() -> str:
    return str(uuid.uuid4())


#loads use from the data base
@login_manager.user_loader
def load_user(user_id: str) -> User:
    user_data = db['users'].find_one({"username": user_id})

    if user_data:
        return User(is_authenticated=True, user_id=user_data["username"])

    return None


#default route
@app.route("/")
def hello_world() -> jsonify:
    app.logger.info("Index route was hit")
    return jsonify({"message": "Hello, World!"}), 200


#signup route if user does not have an account
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
            # hash password
            login_user(user, remember=True)
            add_user_to_active_users(user)
            app.logger.info("create_user() - User created and added to database successfully")
            return jsonify({"message": "User created successfully"}), 201 # This is the status code for created
        except Exception as e:
            app.logger.error(f"create_user() - Error inserting user into database - {e}")
            return jsonify({"error": "Bad request"}), 400
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return jsonify({"error": "Internal server error"}), 500
    

#login route - checks for valid username and password
@app.route('/login', methods=["POST"])
def login() -> jsonify:
    app.logger.info("/login route was hit, logging in a user")

    try:
        data = request.get_json()
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
        add_user_to_active_users(user)
        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": f"{user.get_id()} logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400

#logout route - logs user out
@app.route('/logout', methods=["POST"])
def logout() -> jsonify:
    print(f"logout route hit")
    app.logger.info("/logout route was hit, logging out a user")
    try: 
        print(f"Inside of try block in logout route")       
        data = request.get_json()
        user = load_user(data.get('username'))
        print(f"User ID: {user.get_id()}")
        logout_user(user)
        # TODO: emit a message to everyone in the server/lobby that this client has left
        app.logger.info(f"logout_user() - {user.get_id()} logged out successfully")
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

#updates active user list
@app.route('/active_users', methods=["GET"])
def update_user_list() -> jsonify:
    if not active_users:  # Check if active_users is populated
        app.logger.error("Error: No active users found.")
        return jsonify({"error": "No active users"}), 500

    app.logger.info("/active_users route was hit, updating the list of active users")
    return jsonify({"active_users": [user.get_id() for user in active_users]}), 200
    
#registers user
@socketio.on('register_user')
def handle_registration(data):
    print(f"handle_connection - event register_user hit - {data}")
    add_user_to_active_users_sockets(load_user(data.get('userID')), request.sid)
    print(f"{data.get('userID')} has connected to the server")
    print(f"Active Users: {active_user_sockets}")
    emit("user_joined", data.get('userID'), broadcast=True)


@socketio.on('logout_user')
def log_out(user):
    print(f"{user} is disconnecting from the server")
    emit("user_left", user, broadcast=True)

#keeps track of who invited who and stores data for later use
@socketio.on('send_invite')
def handle_send_invite(data):  # send the invite to the invitee
    inviter = data.get('inviter')
    invitee = data.get('invitee')

    invitee_socket_id = active_user_sockets[str(invitee)]
    app.logger.info(f"{inviter} has sent an invite to {invitee}")
    socketio.emit('invite_recieved', {"inviter": inviter}, to=invitee_socket_id)


#handle invite response and logs the data
@socketio.on('invite_response')
def handle_respond_invite(data):   # send the response from the invitee back to the inviter
    invitee = data.get('invitee')
    inviter = data.get('inviter')
    response = data.get('response')

    app.logger.info(f"{invitee} has {response} {inviter}'s invite")

    if (response == "accepted"):
        game_id = generate_game_ID()
        app.logger.info(f"Game ID for {inviter} and {invitee}: {game_id}")
        socketio.emit('handle_invite_response', {"invitee": invitee, "inviter": inviter, "response": response, "game_id": game_id})
    else:
        socketio.emit('handle_invite_response', {"invitee": invitee, "inviter": inviter, "response": response})
    

#creates a new game when user's invite is accepted
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
        games[game_id] = game.Game(game_id, player1, player2)

    socketio.emit("game_created", {"game_id": game_id}, to=player1_socketID)
    socketio.emit("game_created", {"game_id": game_id}, to=player2_socketID)

#joins the users to a new room
@socketio.on('join_game')
def join_a_game(data):
    game_id = data.get('gameId')
    username = data.get('user')
    join_room(game_id)
    print(f"{username} has joined game room with an id of {game_id}")
    emit('load_board', {'board': games[game_id].get_game_board(), 'user' : username}, to=game_id)


#handles making a move on the backend by checking winning conditions
@socketio.on('make_move')
def make_a_move(data):
    print(request)
    game_id = data.get('game_id')

    # rooms(get his socket id) this will return the list of rooms the player is in. Ideally list of 1, grab that and update the board for that game

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

#makes a new game if players want to play again #sending twice from client??
@socketio.on('new_game')
def play_again(data):
    game_id = data['game_id']
    games[game_id].reset_game_board()


if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname()) # "0.0.0.0"

    if "-p" in sys.argv:
        port_number = int(sys.argv[sys.argv.index("-p") + 1])
    else:
        port_number = 5000

    update_env_file(ip_address, port_number)
    if run_server_tests() is True:
        socketio.run(app, host=ip_address, port=port_number, debug=True)  # Run all of different routes and our API
    else:
        quit()