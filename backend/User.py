##
# @file User.py
# 
# @brief Defines the user class.
# 
# This is the class for how we keep track of who is doing what on the backend.

class User():

    # User constructor, created whenever a user signs up or logs in
    def __init__(self, is_authenticated, user_id):
        self._id = user_id  # this is the username of the user. Which can be used to identify them in the DB and here
        self._is_authenticated = is_authenticated
        self._is_active = True
        self._is_anonymous = False
    

    # Necessary property for working with Flask
    @property
    def is_authenticated(self):
        return self._is_authenticated
    

    # Necessary property for working with Flask
    @property
    def is_active(self):
        return self._is_active
    

    # Necessary property for working with Flask
    @property
    def is_anonymous(self):
        return self._is_anonymous


    # get_id()
    # @param None
    # @return The username of the user object, which is what we use to uniquely identify
    # each user.
    def get_id(self):
        return self._id
    

    # get_is_authenticated()
    # @param None
    # @return A boolean value if the user is authenticated or not.
    def get_is_authenticated(self):
        return self._is_authenticated
    