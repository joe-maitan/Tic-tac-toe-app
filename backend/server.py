##
# @file server.py
# 
# @brief Defines the server class.
# 
# This is the server class. It boots up the Flask app
# and processes all of the routes we have programmed on the client

# imports
import sys
import os
import socket
import uuid
import game
import subprocess

from flask import request, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from flask_socketio import send, emit, join_room, leave_room, rooms
from config import socketio, app, login_manager, db
from User import *


active_user_sockets = {}  # Dictionary of active users {user_id: "socket_id"}
active_users = []  # List of active user objects
games = {}  # Dictionary of games {game_id: game_object}


# update_env_file(host, port)
# @param host, A String for the name of the host
# @param port, A String for the port number the host is running on
# @brief Because the server can be dynamically allocated, we needed a way to tell clients how to connect to the API.
# @return None
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
    if os.environ.get("RUNNING_TESTS") == "1":
        # this is to fix the issue of the tests running recursively
        return True

    os.environ["RUNNING_TESTS"] = "1"  # Mark tests as running

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            text=True  # Ensures output is handled as text, not bytes
        )

        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred while running tests: {e}")
        return False


# add_user_to_active_users(user)
# @param user, a user object
# @brief Adds the user object to the active users list if they are not in the list
# @return None
def add_user_to_active_users(user: User) -> None:
    if user not in active_users:
        active_users.append(user)
    else:
        print(f"User {user.get_id()} is already in the active users list.")


# add_user_to_active_users(user)
# @param user, a user object
# @param socket_id, A string that represents the socket id
# @brief pairs the user object to that socket id that sent the registration request, if they are already in the list, update the socketID
# @return None
def add_user_to_active_users_sockets(user: User, socket_id: str) -> None:
    if user not in active_user_sockets:
        active_user_sockets[user.get_id()] = socket_id
    else:
        print(f"User {user.get_id()} is already in the active user sockets list.")


# generate_game_ID() 
# @param None
# @brief Generates a unique game ID for the new game created
# @return The unique game ID
def generate_game_ID() -> str:
    return str(uuid.uuid4())


# load_user(user_id)
# @param user_id This is the users username that we use to uniquely identify them
# @return A user object with that user id stored or None if we dont have a user with that 
# username in our database
@login_manager.user_loader
def load_user(user_id: str) -> User:
    user_data = db['users'].find_one({"username": user_id})

    if user_data:
        return User(is_authenticated=True, user_id=user_data["username"])

    return None


# hello_world()
# @brief default app route for testing the website
@app.route("/")
def hello_world() -> jsonify:
    app.logger.info("Index route was hit")
    return jsonify({"message": "Hello, World!"}), 200


# create_user()
# @param None
# @brief This is the function for our app route of signup. This route only takes POST requests and will return whatever message
# appropriate based on the criteria. This function is in charge of creating the users account if the account does not exist, email is not 
# already in use, and username is not already in use.
# @return A jsonify object with the appropriate response message and status code
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
              
        hashed_password = password

        newUser = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        # inserts new user into the database, so they can login when they visit the database next time
        try:
            db['users'].insert_one(newUser)
            user = load_user(db['users'].find_one({"username": username})["username"])
            login_user(user, remember=True)
            add_user_to_active_users(user)
            app.logger.info("create_user() - User created and added to database successfully")
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            app.logger.error(f"create_user() - Error inserting user into database - {e}")
            return jsonify({"error": "Bad request"}), 400
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return jsonify({"error": "Internal server error"}), 500
    

# def login()
# @param None
# @brief This is the function responsible for handling our login logic. This checks if a user exists in our system (does the username and password match)
# @return a jsonify response based on the criteria met
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
        
        searched_user_password = searched_username.get("password")
        #if hashlib.sha256(password.encode()) != searched_user_password:
        if password != searched_user_password:
            return {"error": "Invalid password"}, 400
        
        
        user = load_user(searched_username["username"])
        login_user(user, remember=True)
        add_user_to_active_users(user)
        app.logger.info("login_user() - User logged in successfully")
        return jsonify({"message": f"{user.get_id()} logged in successfully"}), 201
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


# logout_user(user)
# @param a user Object that we use to check if the user is a active user.
# @brief if the user object is in either of the lists, this function will remove them from those lists
# @return None
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


# def logout()
# @param None
# @brief This is the function responsible for handling our logout logic. We use logout_user(user) to help with this logic.
# @return a jsonify response based on if the user was able to successfully log out or not.
@app.route('/logout', methods=["POST"])
def logout() -> jsonify:
    print(f"logout route hit")
    app.logger.info("/logout route was hit, logging out a user")
    try: 
        print(f"Inside of try block in logout route")       
        data = request.get_json()
        user = load_user(data.get('user_id'))
        print(f"User ID: {user.get_id()}")
        logout_user(user)
        app.logger.info(f"logout_user() - {user.get_id()} logged out successfully")
        return jsonify({"message": f"{user.get_id()} logged out successfully"}), 200
    except Exception as e:
        app.logger.error(f"logout_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400
       

# profile()
# @brief another method/route made for testing the Flask app
@app.route('/profile', methods=["GET"])
@login_required
def profile() -> jsonify:
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        return jsonify({"user_id": user_id, "is_authenticated": current_user.is_authenticated}), 200
    else:
        return jsonify({"error": "User not authenticated"}), 401


# update_user_list()
# @param None
# @brief This route is responsible for querying the backend to get the current list of active users with every render
# of the lobby page.
# @return a jsonify object with the appropraite message based on if there are active users or not
@app.route('/active_users', methods=["GET"])
def update_user_list() -> jsonify:
    if not active_users:  # Check if active_users is populated
        app.logger.error("Error: No active users found.")
        return jsonify({"error": "No active users"}), 500

    app.logger.info("/active_users route was hit, updating the list of active users")
    return jsonify({"active_users": [user.get_id() for user in active_users]}), 200
    

# handle_registration(data)
# @param data, this is the data that is being sent with the socket event 'register_user'
# @brief This registers the user who sent this request with that socket id that sent the request.
# @return another socket event depending on successful or unsuccessful registration of the user
@socketio.on('register_user')
def handle_registration(data):
    print(f"handle_connection - event register_user hit - {data}")
    add_user_to_active_users_sockets(load_user(data.get('userID')), request.sid)
    print(f"{data.get('userID')} has connected to the server")
    print(f"Active Users: {active_user_sockets}")
    emit("user_joined", data.get('userID'), broadcast=True)


# broadcast_logout(user)
# @param user, which is the username of the user disconnecting
# @brief this function is responsible for broadcasting to all the other users connected that
# this specific user has left the server
# @return None
@socketio.on('logout_user')
def broadcast_logout(user):
    print(f"{user} is disconnecting from the server")
    emit("user_left", user, broadcast=True)


# handle_send_invite(data)
# @param data, which is the data recieved from the socket
# @brief This method handles the sending of invitations. This is done by grabbing the username of the inviter and invitee,
# checking through the active users list, grabbing the invitee's socketID and sending the invite recieved event to them
# specifically, letting them know who invited them.
# @return 'invite_recieved' socket event
@socketio.on('send_invite')
def handle_send_invite(data):  # send the invite to the invitee
    inviter = data.get('inviter')
    invitee = data.get('invitee')

    invitee_socket_id = active_user_sockets[str(invitee)]
    app.logger.info(f"{inviter} has sent an invite to {invitee}")
    socketio.emit('invite_recieved', {"inviter": inviter}, to=invitee_socket_id)


# handle_respond_invite(data)
# @param data, which is the data recieved from the socket
# @brief depending on if the invite is accepted or declined two different events will happen. If accepeted, a game is created and the
# event 'handle_invite_response' carries an additional property of game id to redirect the client to. Else, the client is notified that
# the person they invited has declined their invite and they stay in the lobby.
# @return 'handle_invite_response' event depending on if the invitee accepeted or declined the invite
@socketio.on('invite_response')
def handle_respond_invite(data):
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
    

# create_a_game(data)
# @param data, which is the data recieved from the socket
# @brief creates a game with the username and socket id's of both players thanks to the invite response. This creation of the game lets
# the client-side know to now imply the rules of the game/lets both players actually play now.
# @return 'game_created' socket event.
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


# join_a_game(data)
# @param data, which is the data recieved from the socket
# @brief after game creation, the players join the game. We group them to this common room thanks to the unique game ID generated.
# every room is unique to every game.
# @return 'load_board' event to the game_id where both players will be notified of the board.
@socketio.on('join_game')
def join_a_game(data):
    game_id = data.get('gameId')
    username = data.get('user')
    join_room(game_id)
    print(f"{username} has joined game room with an id of {game_id}")
    emit('load_board', {'board': games[game_id].get_game_board(), 'user' : username}, to=game_id)


# make_a_move(data)
# @param data, which is the data recieved from the socket
# @brief This is where the game between the players is played out. This manages turns and win conditions. After every move a 'move_made'
# event is emitted to the client so that the game on that end is correctly updated.
# @return 'move_made' event, prompting the client side to update their board.
@socketio.on('make_move')
def make_a_move(data):
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


# play_again(data)  
# @param data, which is the data recieved from the socket
# @brief When the players are prompted to play again, this resets the board of the game room they are currently in and resets whose turn it is.
# @ return None
@socketio.on('new_game')
def play_again(data):
    # possibly being sent twice from the client??
    game_id = data['game_id']
    games[game_id].reset_game_board()


if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname()) # "0.0.0.0"

    if "-p" in sys.argv:
        port_number = int(sys.argv[sys.argv.index("-p") + 1])
    else:
        port_number = 5000

    update_env_file(ip_address, port_number)
    if run_server_tests():
        app.logger.info(f"Passed all unit tests. Running server logic...")
        socketio.run(app, host=ip_address, port=port_number, debug=True)  # Run all of different routes and our API