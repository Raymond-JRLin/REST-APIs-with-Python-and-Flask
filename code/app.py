from flask import Flask
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
        item = {'name': name, 'price': 12.00}
        items.append(item) # add it into items list
        return item, 201 # tell client it succeeds
        # 200 OK is for when the server just kind of returns some data, and everything's ok and I've given what you wanted
        # 201 CREATED is for created
        # 202 ACCEPTED is when you are delaying the creation, tells client server would create it like 5 or 10 minutes later, it may fail but it's out of client's control

        # so it's important to use correct status code for client to check whether things went wrong or not

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf

app.run(port = 5000)
