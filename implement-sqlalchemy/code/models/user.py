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
