##
# @file config.py
# 
# @brief Defines the config for the Flask app.

# Imports
from pymongo import MongoClient
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_login import LoginManager
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' 

socketio = SocketIO(app, cors_allowed_origins="*", manage_session=True, logger=True) # the only accepted origin is our front end server
CORS(app, origins='*', supports_credentials=True)

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app.logger.info("congfig.py - Flask app created")
app.logger.info("congfig.py - Establishing connection to database")

try:
    client = MongoClient('mongodb+srv://erinktaketa:Tictactoe123!@tictactoedb.l8kom.mongodb.net/?retryWrites=true&w=majority&appName=TicTacToeDB')
    app.logger.info("congfig.py - Successfully connected to database.")
except Exception as e:
    app.logger.error("congfig.py - Error connecting to database.")
    app.logger.error(e)
    exit(1)

db = client['TicTacToeDB']

try:
    db['users'].create_index("username", unique=True)
    db['users'].create_index("email", unique=True)
except Exception as e:
    app.logger.error("congfig.py - Error creating user collection.")
    app.logger.error(e)
    exit(1)

login_manager = LoginManager()
login_manager.init_app(app)