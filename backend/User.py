from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, is_authenticated, user_id):
        self._id = user_id  # this is the username of the user. Which can be used to identify them in the DB and here
        self._is_authenticated = is_authenticated
        self._is_active = True
        self._is_anonymous = False
    

    @property
    def is_authenticated(self):
        return self._is_authenticated
    

    @property
    def is_active(self):
        return self._is_active
    

    @property
    def is_anonymous(self):
        return self._is_anonymous


    def get_id(self):
        return self._id  # returns the username of the user
    

    def get_is_authenticated(self):
        return self._is_authenticated