from flask import request
from config import app, db
from models import User

# CONVETION: AVOID VERBS IN THE ROUTES
# PLURAL NOUNS ARE PREFFERED
# USE DIFFERENT METHODS TO INDICATE WHAT THE ACTION IS DOING

# @app.route('/)
# greet the user


@app.route('/user', methods=["POST"])
def create_user():
    # creates a user object with a username, email, and password. This is how they will be identified in the system
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "Missing username, email, or password"}, 400
    
    hashed_password = password  # hash the password

    newUser = User(username=username, email=email, password=hashed_password)
    db.session.add(newUser)
    db.session.commit()



@app.route('/user', methods=["GET"])
def login_user():
    # logs in a user assumming the input username and password match with a username and password
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    queried_username = User.query.filter_by(username=username).first()    
    queried_password = User.query.filter_by(password=password).first()

    if not queried_username or not queried_password:
        return {"error": "User not found"}, 404

    


@app.route('/logout', methods=["GET"])
def logout_user():
    # logs out a user
    pass


@app.route("/invite_user", methods=["POST"])
def invite_user():
    # invites a user to play a game
    pass


# @app.route('/play_game') with another user

# @app.route('/play_game_with_bot')


if __name__ == "__main__":
    with app.app_context():  # When we are about to run the app, we create the models defined in the database, if they are not already created
        db.create_all()

    app.run(debug=True)  # Run all of different routes and our API