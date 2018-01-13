import sqlite3
from db import db

# we moved User class from user.py of resource package to here - user.py of model package, because it's not a resource, which means API cannot receive data into this class or send this class as a JSON representation. It's a helper essentially, which we use to store some data about the User and also a helper that contains a couple of methods to allow us to easily retrieve User objects from a database

# model is our internal representation of an entity, whereas a resource is the external representation of an entity

class UserModel(db.Model):
    __tablename__ = 'users'

    # tell SQLAlchemy 3 columns the model is going to have, when we do saving, only going to look for these 3 properties even though there's something else in __init__ and it won't be save into database
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80)) # 80 character maximum to limit the size
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db') # initialize a connection
        cursor = connection.cursor() # initialize a cursor

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,)) # don't forget the input is a tuple, even though thers's only one parameter, we'll still use a comma
        row = result.fetchone() # get the 1st row
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row) # assign the whole row values
        else:
            user = None

        # no commit since we don't need to write into database
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db') # initialize a connection
        cursor = connection.cursor() # initialize a cursor

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,)) # don't forget the input is a tuple, even though thers's only one parameter, we'll still use a comma
        row = result.fetchone() # get the 1st row
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        # no commit since we don't need to write into database
        connection.close()
        return user
