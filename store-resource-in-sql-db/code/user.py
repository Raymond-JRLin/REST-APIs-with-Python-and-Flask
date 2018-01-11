import sqlite3
from flask_restful import Resource, reqparse

class User:
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

# create a new class for user to register into database
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be blank."
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)" # because we use system's id with automatic incremental, keep id as NULL
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully.'}, 201
