from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


# many REST APIs just like CRUD APIs: create, read, update, delete

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True, #ensure no request can come throught with no price
        help = "This field cannot be left blank!"
    )

    @jwt_required()
    # we have to authenticate before we can call the get method
    def get(self, name):
        ### retrieve items from database
        # item = next(filter(lambda x : x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        ###

        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    # use a class method so we don't need to do the same thing in different methods
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        ### retrieve items from database
        # improvement: to make sure there's only unique names for items
        # if next(filter(lambda x : x['name'] == name, items), None) is not None:
        #     # there's an item having the name
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        ###

        # make sure the item is not already in database first
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # 400: when something did go wrong with the request

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        ### now write into database
        # items.append(item) # add it into items list
        ###

        # and make insertion as a single method outside of POST so we can also call insertion method in PUT
        # it may have problem to insert an item, so we use try to catch exception if it raised
        try:
            self.insert(item)
        except Exception as e:
            return {'message': "An error occurred inserting the item."}, 500 # 500: Internal Server Error, something went wrong but we can't tell you exactly what - something didn't go wrong with the request but the server messed up

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        ### with db
        # global items
        # items = list(filter(lambda x : x['name'] != name, items))
        ###

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?" # delete one row
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        ### retrieve from database
        # item = next(filter(lambda x : x['name'] == name, items), None)
        ###
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            # create a new item
            # item = {'name': name, 'price': data['price']}
            # item.append(item)
            try:
                self.insert(updated_item)
            except Exception as e:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except Exception as e:
                return {"message": "An error occurred updating the item."}, 500

        return updated_item # return the new one

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name'])) # match the values in-order

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        ### retrieve from database
        # return {'items': items}
        ###
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items =[]
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
