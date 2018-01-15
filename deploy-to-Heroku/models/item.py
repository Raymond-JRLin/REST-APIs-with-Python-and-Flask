# import sqlite3 # we don't need sqlite3 any longer since we use SQLAlchemy
from db import db

class ItemModel(db.Model):
    # specify table name and columns
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80)) # 80 character maximum to limit the size
    price = db.Column(db.Float(precision = 2)) # 2 numbers after the decimal point

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # add a store id to link the items and its belonging store
    store = db.relationship('StoreModel') # how SQLAlchemy does join

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # return a JSON representation of model, basically a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # move following methods from item.py in resource to here, models, since they don't belong to a resource
    # keep this as class method since it will return a dictionary other than a model object
    @classmethod
    def find_by_name(cls, name):
        ### use SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(*row) # parse all elements in row to a item model
        ###

        # SQLAlchemy will transit a row to ItemModel if it can, .query is using a query builder
        # return ItemModel.query.filter_by(name = name).first()
        return cls.query.filter_by(name = name).first() # SELECT * FROM items WHERE name = name LIMIT 1
        # return a item model object

    # modify following 2 methods as not class method since they can use item model object directly
    def save_to_db(self):
        ### use SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()
        ###
        # save the model into database, SQLAlchemy can automatically translate model to row in a database, so we just tell it the object - self
        db.session.add(self)
        db.session.commit()
        # it can update so we change this method to do insertion and updating, then we don't need another separate update method but we create another delete_from_db method for better use

    ### don't need
    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items SET price = ? WHERE name = ?"
    #     cursor.execute(query, (self.price, self.name)) # match the values in-order
    #
    #     connection.commit()
    #     connection.close()
    ###
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
