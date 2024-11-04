import pymongo
import os
from pymongo import MongoClient

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_login import LoginManager
# from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #os.u_random(100)
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
# app.config['SESSION_PERMANENT'] = False  # Non-permanent session

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173") # the only accepted origin is our front end server
CORS(app, origins='*', supports_credentials=True)

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