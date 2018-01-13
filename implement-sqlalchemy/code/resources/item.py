from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        # make sure the item is not already in database first
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # 400: when something did go wrong with the request

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except Exception as e:
            return {'message': "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        ### use SQLAlchemy
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name = ?" # delete one row
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}
        ###

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            ### use SQLAlchemy
            # try:
            #     updated_item.insert()
            # except Exception as e:
            #     return {"message": "An error occurred inserting the item."}, 500
            ###
            item = ItemModel(name, data['price'])
        else:
            ### use SQLAlchemy
            # try:
            #     updated_item.update()
            # except Exception as e:
            #     return {"message": "An error occurred updating the item."}, 500
            ###
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        ### use SQLAlchemy
        # ### retrieve from database
        # # return {'items': items}
        # ###
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        #
        # items =[]
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        # return {'items': items}
        ###

        # return {'item': [item.json() for item in ItemModel.query.all()]} # remember to return a JSON
        # or we do this by lambda function
        # return {'items': list(map(lambda x : x.json(), ItemModel.query.all()))} # use map to do mapping
        # or
        return {'items': [x.json() for x in ItemModel.query.all()]}
