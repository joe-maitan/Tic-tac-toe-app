from bson.objectid import ObjectId


class Post:

    def __init__(self, username, email, password, _id=None):
        self._id = _id if _id else ObjectId()
        self.username = username
        self.email = email
        self.password = password
    
    
    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
    
    
    @staticmethod
    def from_dict(data):
        return Post(
            _id=data.get("_id"),
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
    
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"