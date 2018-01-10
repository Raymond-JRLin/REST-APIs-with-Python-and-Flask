from flask import Flask, request
from flask_restful import Resource, Api
# resource is a thing can be created and changed by API
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Raymond' # use a secret key and JWT, which stands for JSON Web Token, to encrypt message -> add security.py
api = Api(app)

jwt = JWT(app, authenticate, identity) # JWT creates a new endpoint of /auth, including a user name and password, then JWT sent them to authenticate function to compare, and returns a JW token. JWT itself can do nothing, but send to identity function

items = []

class Item(Resource):
    @jwt_required()
    # we have to authenticate before we can call the get method
    def get(self, name):
        ###
        # for item in items:
        #     if item['name'] == name:
        #         return item # we don't need jsonify because restful does that for us
        ###
        # improvement: use Lambda funtion
        item = next(filter(lambda x : x['name'] == name, items), None) # lambda returns not a item or list but lambda object, so we can return a list of items whose names match the searching name, e.g.: list(filter(lambda x : x['name'] == name, items)). But we know there's exact only one item having the given name, so we use next to return the first item found by this filter funtion. Similarly, we can use one more next to get 2nd mathced item and then 3rd and so on. But it may raise a problem if there's no such matched item left, then next would break our program. So we set a default value as None, which means if there's no matched item, then return none
        # return {'item': None}, 404 # return a JSON
        # 200 is the most popular http status code, but 404 NOT FOUND is the correct one for not found
        # return {'item': item}, 200 if item is not None else 404
        # shorten:
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # improvement: to make sure there's only unique names for items
        if next(filter(lambda x : x['name'] == name, items), None) is not None:
            # there's an item having the name
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # 400 is bad request, because it's not our fault but client's since they should have verified it's not an existing name, but we can tell them it's an invalid input because it's already in this app

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
