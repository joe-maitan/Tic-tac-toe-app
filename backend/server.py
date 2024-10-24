from flask import request
from config import app, mongo
from werkzeug.security import generate_password_hash, check_password_hash

# CONVETION: AVOID VERBS IN THE ROUTES
# PLURAL NOUNS ARE PREFFERED
# USE DIFFERENT METHODS TO INDICATE WHAT THE ACTION IS DOING

@app.route('/')
def index():  # greet the user at the index
    app.logger.info("client has joined. Index route was hit")
    # render_template("index.html")
    pass


@app.route('/user', methods=["POST"])
def create_user():
    app.logger.info("/signup route was hit, creating a new user")

    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            app.logger.error("create_user() - Missing username, email, or password")
            return {"error": "Missing username, email, or password"}, 400
        
        existing_email = mongo.db.users.find_one({"email": email})
        existing_username = mongo.db.users.find_one({"username": username})
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

        mongo.db.users.insert_one(newUser)

        app.logger.info("create_user() - User created successfully")    
        return {"message": "User created successfully"}, 201
    # TODO: after creation/log in, redirect them to the game/lobby page
    except Exception as e:
        app.logger.error(f"create_user() - Error creating user {e}")
        return {"error": "Internal server error"}, 500
    
    
@app.route('/user', methods=["GET"])
def login_user():
    app.logger.info("/login route was hit, logging in a user")

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        searched_email = mongo.db.users.find_one({"email": email})

        if not searched_email:
            return {"error": "User not found"}, 404
        
        if searched_email.get("password") != password:
            return {"error": "Invalid password"}, 400

        app.logger.info("login_user() - User logged in successfully")
        # TODO: after creation/log in, redirect them to the game/lobby page
    except Exception as e:
        app.logger.error(f"login_user() - Error parsing JSON {e}")
        return {"error": "Invalid JSON"}, 400


    
    
@app.route('/user', methods=["GET"])
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
    # TODO: HOOK UP DATABASE PROPERLY IN server.py
    # with app.app_context():  # When we are about to run the app, we create the models defined in the database, if they are not already created
    #     # db.create_all()
    # initialize mongoDB database here?

    app.run(debug=True)  # Run all of different routes and our API