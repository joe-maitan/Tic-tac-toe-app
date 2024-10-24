import pymongo

from pymongo import MongoClient

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


app.logger.info("congfig.py - Flask app created")
app.logger.info("congfig.py - Establishing connection to database")

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['TestTicTacToeDB']
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
# app.config['MONGO_DBNAME'] = 'TestTicTacToeDB'


try:
    client.admin.command('ping')
    app.logger.info("congfig.py - Successfully connected to database.")
except Exception as e:
    app.logger.error("congfig.py - Error connecting to database.")
    app.logger.error(e)