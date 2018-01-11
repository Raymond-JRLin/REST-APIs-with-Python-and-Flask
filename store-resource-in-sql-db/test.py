import sqlite3 # already in Python, able to connect and run queries

# build a connection between sqlite db and Python
connection = sqlite3.connect('data.db') # connection string - URI: Unified Resource Identifier

cursor = connection.cursor() # select and start things, responsible for quering and store the results

# create a table
create_table = "CREATE TABLE users (id int, username text, password text)" # <table_name> (<columns>)
cursor.execute(create_table)

# insert a tuple
user = (1, 'Raymond', 'ray') # Python tuple
insert_query = "INSERT INTO users VALUES (?, ? , ?)" # insert query: <table_name> (<id>, <user_name>, <password>)
cursor.execute(insert_query, user) # it can replace question marks smartly

# use list of tuples to insert bunch of users
users = [
    (2, 'jose', 'asdf'),
    (3, 'rolf', 'xyz')
]
cursor.executemany(insert_query, users)

# retrieve data
select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

# save to disc
connection.commit()

connection.close() # close the connection to stop receiving command
