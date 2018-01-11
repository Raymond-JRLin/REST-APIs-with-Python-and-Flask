import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    # return a JSON representation of model, basically a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # move following methods from item.py in resource to here, models, since they don't belong to a resource
    # keep this as class method since it will return a dictionary other than a model object
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row) # parse all elements in row to a item model 

    # modify following 2 methods as not class method since they can use item model object directly
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.price, self.name)) # match the values in-order

        connection.commit()
        connection.close()
