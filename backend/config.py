import pymongo
from pymongo import MongoClient

from flask import Flask
from flask_cors import CORS

from flask_login import LoginManager
# import database.users # from database import users

app = Flask(__name__)

CORS(app)

app.logger.info("congfig.py - Flask app created")
app.logger.info("congfig.py - Establishing connection to database")

try:
    client = MongoClient('mongodb+srv://erinktaketa:Tictactoe123!@tictactoedb.l8kom.mongodb.net/?retryWrites=true&w=majority&appName=TicTacToeDB')
    # client = MongoClient(host='tictactoedb-shard-00-00.l8kom.mongodb.net', port=27017, username='erinktaketa', password='Tictactoe123!')
    app.logger.info("congfig.py - Successfully connected to database.")
except Exception as e:
    app.logger.error("congfig.py - Error connecting to database.")
    app.logger.error(e)
    exit(1)

db = client['TicTacToeDB']

# db['users'].insert_one({"username": "test", "email": "test@email.com", "password": "test"})
# db['users'].insert_one({"username": "jjmaitan", "email": "test@email.com", "password": "test"})

try:
    # db.create_collection('users')
    db['users'].create_index("username", unique=True)
    db['users'].create_index("email", unique=True)
except Exception as e:
    app.logger.error("congfig.py - Error creating user collection.")
    app.logger.error(e)
    exit(1)


login_manager = LoginManager()
login_manager.init_app(app)