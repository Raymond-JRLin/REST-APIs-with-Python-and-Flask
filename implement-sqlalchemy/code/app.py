from flask import Flask
from flask_restful import Api
# resource is a thing can be created and changed by API
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # in order to know when an object had changed but not been saved to database, the extension flask_sqlalchemy was tracking every change that we made to the SQLAlchemy session, and that took some resources. We turns off flask_sqlalchemy modification tracker but not turns off SQLAlchemy modification tracker because SQLAlchemy itself, the main library, has its own modification tracker, which is a bit better. Just change the extension behaviours
app.secret_key = 'Raymond' # use a secret key and JWT, which stands for JSON Web Token, to encrypt message -> add security.py
api = Api(app)

jwt = JWT(app, authenticate, identity) # JWT creates a new endpoint of /auth, including a user name and password, then JWT sent them to authenticate function to compare, and returns a JW token. JWT itself can do nothing, but send to identity function


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register') # added /register endpoint

if __name__ == '__main__':
    # import here to prevent circular import when we import Item and User model
    from db import db
    db.init_app(app)
    # prevent running this app.py when we just import it
    app.run(port = 5000, debug = True) # Flask is nice to show the error message
