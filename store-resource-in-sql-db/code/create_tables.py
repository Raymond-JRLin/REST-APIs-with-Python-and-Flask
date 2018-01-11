import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" # use INTEGER to make it incremental autmatically
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, password real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()

connection.close()
