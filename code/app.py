from flask import Flask, request
from flask_restful import Resource, Api
# resource is a thing can be created and changed by API

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item # we don't need jsonify because restful does that for us
        return {'item': None}, 404 # return a JSON
        # 200 is the most popular http status code, but 404 NOT FOUND is the correct one for not found

    def post(self, name):
        # pass JSON payload, but there would be some problem if it's not a JSON or there's no header or body. There's 2 ways to handle:
        # method 1:
        # data = request.get_json(force = True) # you don't need the content-type header just look the content and format it even if the content-type is not set to be application/JSON
        # but it's dangerouse since if you don't use that it will look into header and get an error, if you use that, it will not look in header and get even incorrect content
        # method 2:
        # data = request.get_json(silent = True) # it doesn't give an error, it just basically returns none
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item) # add it into items list
        return item, 201 # tell client it succeeds
        # 200 OK is for when the server just kind of returns some data, and everything's ok and I've given what you wanted
        # 201 CREATED is for created
        # 202 ACCEPTED is when you are delaying the creation, tells client server would create it like 5 or 10 minutes later, it may fail but it's out of client's control

        # so it's important to use correct status code for client to check whether things went wrong or not

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')

app.run(port = 5000, debug = True) # Flask is nice to show the error message
