# Tic-tac-toe-app

## Python Version and Software
We used a version of Python that was at 3.10 or greater. To load python 3.10 on the CSU CS machines run the following command:
```
module load python/bundle-3.10
```

If you have another version of Python installed greater than 3.10 do not worry about running the module load command.

We developed this using Google Chrome, finding it was the most friendly web browser for our login/signup forms and debugging our game logic.

# Sprints
## Sprint 1 - Implement Client and Server architecture
1. Basic Server Setup:
   - The backend Server runs a flask app that processes requests and socket events.
2. Client-Side connection
   - The client is a web browser that can be booted up by running the client script as shown below. This will connect them to the backend server.
   - When the client is on the web page they are greated with a sign up/ log in page where they will need to create an account that is stored in our database managed by the backend.
   - Once the client has created an account or logged in, they wait in the lobby waiting to invite other players.
3. Simple Message Exchange
   - Use of HTTP requests for logging in and signing up, logging out, getting the list of active users. They can invite other players through the use of SocketIO.
4. Error Handling
5. Testing and Debugging:
   - Server can handle multiple client connections and distinguish their socket ID's from one another.
   - Client can exchange messages to the server and they will be processed accordingly.

## Sprint 2 - Design and Implement Message Protocol
1. Game-Message Protocol Specification:
   - The client has two ways of sending messages to the server. The first is through HTTP requests and the second through SocketIO.
   - The HTTP requests manage signing up or logging the user in, logging them out, getting a list of active users.
   - The SocketIO manages the events of inviting another player and taking a turn in game.
2. Server-Side Message Handling:
   - The server parses all HTTP requests and specific SocketIO events. The data sent from either a request or socket event is a JSON object that we can parse in python, and then the response sent back is a dictionary with unique fields for each response.
3. Client-Side Message Handling:
   - As stated above, the client has two ways of sending messages to the server. The first is through HTTP requests and the second through SocketIO.
   - The HTTP requests manage signing up or logging the user in, logging them out, getting a list of active users.
   - The SocketIO manages the events of inviting another player and taking a turn in game.
4. Connection Management:
   - Everytime a user makes it to the lobby, they register into the backend server, where we add them into the active users list with their username and SocketID, this way we can keep track of disconnections and logouts.
   - When a user disconnects or logouts, they are deregistered from the server, which removes them from the active users list.

## Sprint 3 - Multiplayer Functionality
- Clients can invite eachother through the use of SocketIO. The invite mechanism is handled on the backend and then forwarded to the invitee's socket where a pop up will prompt them to accept or decline the invite.
- If accepted a new game object is created where it will pick a player to go first, following the rules of tic tac toe, until there is a winner or draw

1. Game State Synchronization:
   - The server creates a new game for each of the invitations accepted and groups those players in that game.
   - Server then handles turn login, updating the board after a turn, and will not allow a player to go if it is not their turn.
2. Client-Side Game Rendering:
   - After accepting an invite, they are brough to a unique game page where they will take turns with their opponnenet until a win or draw.
   - After each turn the board updates on both sides simulatneously through the use of SocketIO
3. Turn-Based Gameplay
   - Server handles turns of the players.
   - Lets a player know if it is not their turn/will not place their symbol on the board until it is their turn.
4. Player Identification:
   - Each player has a unqiue username that is kept in a cookie after logging in or signing up.
   - This is how the server keeps track of whose turn it is.

## Sprint 4 - Gameplay, Gamestate, UI
1. Game State Management
   - Inviter is the first person who can make a move and is always 'X'
   - Server manages game state and whos turn it is. Keeping track of the current player and board state
2. Input Handling:
   - Client can click with a mouse but if it is not their turn, nothing will be placed until the player whose turn it is
    places their symbol.
   - Validate the placement of the symbol by checking if the index is not taken and is in bounds.
4. Winning Conditions:
   - The game can end either in a draw or one player winning. On both conditions a unqiue message is played.
   - Players can opt to play with the same person again, reseting the game board but keeping track of their current symbols.
4. Game Over Handling
   - If a player declines playing again after the match concludes, they are redirected to the lobby. But they can
     opt to play with the same person again.
6. User Interface
   - Use of WebServer UI and images for the Tic Tac Toe symbols.

## Sprint 5 - Error Handling and Testing
1. Error Handling:
   - Client and Server have their own unique try-catch blocks. For example, the server processes the requests but will return an error code if the username they tried to register with is already in the database.
   - Informative error messages will occur if user input is not what was expected like invalid password or username as an example.
   - The Client will throw an error if the request/response is missing data.
   - The server/backend uses pytest to test the functionality of the server/flask app.
   - The app now logs to an app.log file created/overwritten on running the server.py script.
2. Integration Testing
   - Tests gamemoves/updating of the board state is also done with pytest on the backend.
   - Tests invalid moves on the board behave correctly.
   - Tests sign up, login, and logout functions to ensure expected functionality.
3. Security/Risk Evaluation:
   - This development of the Flask App uses HTTP which lacks the encryption/reliability of HTTPS.
   - Users login and sign up information is not encrypted, so you can see their information in cleartext in a console log that we used for debugging. Since nothing is encrypted, you can easily see someone's username, email, or password.
   - The cookie is not encrypted in a safe manner which only stores the username of the user but is still information that is out there for whoever.
   - It could be possible to overload the login/signup requests causing the server to crash because we have no mechanism to stop after a certain number of failed tries.

# How to run the app
Depending on what **version of Python** you have installed/loaded your command will either be **python/pip** or **python3/pip3** respectively. The basis of the commands remains the same
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
* On MacOS, Linux and Windows:
```
python3 -m venv venv
```
NOTE: The venv is NOT included in the code provided.

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
* On MacOS, Linux and Windows:
```
pip3 install -r requirements.txt
```

7. Running the code!
**The Server and Client need to be run on different machines**
* For the backend (server):
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\backend python3 server.py -p <port>
```
This will run all of the backend unit tests we have added as well before launching the server. If you do not specify a port number it will default to 5000.
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\backend python3 server.py
```
* For the frontend (client):
```
C:\Users\jjmai\Documents\GitHub\Tic-tac-toe-app\frontend python3 client.py -i <hostaddress> -p <port>
```
This client command will install all necessary dependencies. When the npm run dev is finished, you can click on the 'Network' option to be visibile to other hosts.

# Where we would take this project
Joe:
- I would try to fix some of the security issues such as being able to spam the login forms.
- I see this project as being a great resume builder as we had to figure out how to set up our own database, learn frontend developement, and learn how to use Flask all in the span of a semester.
- This project has beena culmination of all my skills and I am proud to say I am happy with where it is at.

# Retrospective
## What went right
- The design of the full stack app went really smoothly, besides encountering some weird bugs we kept cruising forward.
- The Sprints were very manageable and the work load was easy to balance.
- We were able to bounce back from a bad start to sprint 2 to having a full-stack Tic Tac Toe application!

## What could have gone better.
- Distributing the work load could have gone a lot better. We should have evenly distributed the work load instead of having only one to two us of working on the project at a time.
- Meeting as a team. After sprint 2 we lacked communication and getting together as a team.
- Learning how to use tools like React in previous classes instead of learning it on the fly. It was a great expereince but some previous knowledge could have made the process go a lot faster.
