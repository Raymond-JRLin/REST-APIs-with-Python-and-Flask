import os

from flask import Flask
from flask_restful import Api
# resource is a thing can be created and changed by API
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # in order to know when an object had changed but not been saved to database, the extension flask_sqlalchemy was tracking every change that we made to the SQLAlchemy session, and that took some resources. We turns off flask_sqlalchemy modification tracker but not turns off SQLAlchemy modification tracker because SQLAlchemy itself, the main library, has its own modification tracker, which is a bit better. Just change the extension behaviours
# deploy in Heroku and use PostgreSQL to store data, so in Heroku we use the OS environment variable, but keep sqlite as second choice when we test locally
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # tell SQLAlchemy where to read our database. Also, it works if we cange sqlite: to MySQL/PostgreSQL
app.secret_key = 'Raymond' # use a secret key and JWT, which stands for JSON Web Token, to encrypt message -> add security.py
api = Api(app)

### since we deploy in Heroku, we would not run this app.py because we run through UWSGI, so there's no db imported then cause a error - cannot run db.create_all(). We cannot import db outside of if structure otherwise we would get circular import, so move it to run.oy
# @app.before_first_request
# # it will run following creating before any request unless there's a table existing
# def create_tables():
#     db.create_all() # it only create what it sees, so it's very important to import store and StoreList
###

jwt = JWT(app, authenticate, identity) # JWT creates a new endpoint of /auth, including a user name and password, then JWT sent them to authenticate function to compare, and returns a JW token. JWT itself can do nothing, but send to identity function

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register') # added /register endpoint


if __name__ == '__main__':
    # import here to prevent circular import when we import Item and User model
    from db import db
    db.init_app(app)
    # prevent running this app.py when we just import it
    app.run(port = 5000, debug = True) # Flask is nice to show the error message
