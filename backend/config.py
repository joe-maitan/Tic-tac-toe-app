import pymongo
from pymongo import MongoClient

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)

app.logger.info("congfig.py - Flask app created")
app.logger.info("congfig.py - Establishing connection to database")

# MongoDB configuration
# client = MongoClient("mongodb://localhost:27017/")  # Connect to TicTacToeDB Connection
# db = client['Users']  # Access the Users database
# collecton = db['users']  # Access the users collection

app.config['MONGO_URI'] = 'mongodb://localhost:27017/TicTacToeDB'
mongo = PyMongo(app)

try:
    # client.admin.command('ping')
    app.logger.info("congfig.py - Successfully connected to database.")
except Exception as e:
    app.logger.error("congfig.py - Error connecting to database.")
    app.logger.error(e)