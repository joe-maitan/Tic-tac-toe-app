from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pymongo.mongo_client import MongoClient

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MongoDB configuration
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/tictactoe'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'

# db = SQLAlchemy(app)

# Initialize MongoDB client
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()

try:
    client.admin.command('ping')
    app.logger.info("Connected to database")
except Exception as e:
    app.logger.error("Error connecting to database")
    app.logger.error(e)