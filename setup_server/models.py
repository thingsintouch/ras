
from datetime import datetime
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

class User(UserMixin):

    def __init__(self, password, id):
        self.password = password
        self.id = id

    def check_password(self, password):
        return (self.password == password)

    def __repr__(self):
        return f"User {self.id}"
