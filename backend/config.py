from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tictactoe'

# db = SQLAlchemy(app)

# Initialize MongoDB client
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()