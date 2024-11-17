# Tic-tac-toe-app
CS457 Term Project

# Python Version and Software
The Python version used for developing this project was 3.11. If you have a greater version than 3.11 everything will work regardless, do not worry about using 3.11 specifically.

To load python 3.11 on the CSU CS machines run the following command:
```
module load python/bundle-3.10
```

# Sprints
## Sprint 1 - Implement Client and Server architecture
- The backend Server runs a flask app that processes requests and socket events.
- The client is a web browser that can be booted up doing the npm run dev command below.
- When the client is on the web page they are greated with a sign up/ log in page where they will need to create an account that is stored in our database managed by the backend.
- Once the client has created an account or logged in, they wait in the lobby waiting to invite other players

## Sprint 2 - Design and Implement Message Protocol
- The client has two ways of sending messages to the server. The first is through HTTP requests and the second through SocketIO.
- The HTTP requests manage signing up or logging the user in, logging them out, getting a list of active users.
- The SocketIO manages the events of inviting another player and making a game move

## Sprint 3 - Multiplayer Functionality
- Clients can invite eachother through the use of SocketIO. The invite mechanism is handled on the backend and then forwarded to the invitee's socket where a pop up will prompt them to accept or decline the invite.
- If accepted a new game object is created where it will pick a player to go first, following the rules of tic tac toe, until there is a winner or draw

## Sprint 4 - Gameplay, Gamestate, UI
1. Game State Management
   - Inviter is the first person who can make a move and is always 'X'
   - Server manages game state and whos turn it is. Keeping track of the current player and board state
2. Input Handling:
  - Client can click with a mouse but if it is not their turn, nothing will be placed until the player whose turn it is
    places their symbol.
  - Validate the placement of the symbol by checking if the index is not taken and is in bounds.
3. Winning Conditions:
  - The game can end either in a draw or one player winning. On both conditions a unqiue message is played.
  - Players can opt to play with the same person again, reseting the game board but keeping track of their current symbols.
4. Game Over Handling
   - If a player declines playing again after the match concludes, they are redirected to the lobby. But they can
     opt to play with the same person again.
5. User Interface
   - Use of WebServer UI and images for the Tic Tac Toe symbols.
## Sprint 5 - Error Handling and Testing
- Backend uses pytest to test the functionality of the server/flask app.

# How to run the app
1. Clone the repository
```
git clone https://github.com/joe-maitan/Tic-tac-toe-app.git
```

2. Navigate to the project directory
```
cd Tic-tac-toe-app
```

3. Navigate to the backend directory
```
cd backend
```

4. Create a virtual enviornment
* On MacOS and Linux
```
python3 -m venv venv
```

* On Windows
```
python -m venv venv
```

NOTE: The venv is already included in the project, just needs to be activated.

5. Activate the virtual enviornment:
* On MacOS and Linux:
```
source venv/bin/activate
```

* On Windows:
```
venv/Scripts/activate
```

6. Install dependencies:
* On MacOS and Linux:
```
pip3 install -r requirements.txt
```

* On Windows:
```
pip install -r requirements.txt
```

7. Navigate to the frontend directory:
```
cd ../frontend
```

8. Running the code!
* For the backend (server):
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\backend python3 server.py <port>
```
* For the frontend (client):
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\frontend python3 client.py
```


