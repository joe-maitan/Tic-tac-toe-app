from config import db

class User(db.model):
    username = None
    email = None
    password = None
