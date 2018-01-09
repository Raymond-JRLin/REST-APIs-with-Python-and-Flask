# the server, the Flask application has to be created to understand requests from browsers

# tell Python we want to use flask
from flask import Flask, jsonify

app = Flask(__name__) # create a Flask object with unique name

# create a list
stores = [
	{
		'name': 'My Wonderful Store',
		'items': [
			{
				'name': 'My Item',
				'price': 15.99
			}
		]
	}
]

###
# # create a route for homepage
# @app.route('/') # end-point with /
# def home():
# 	# return a response to browsers
# 	return "Hello, world!"
###

# from server perspective:
# POST: used to recerive data
# GET: used to send data back only

# POST /store data: {name: }
@app.route('/store', methods = ['POST']) # default rout is a GET
def create_store():
	pass

# GET /store/<string: name>
@app.route('/store/<string:name>') # 'http://127.0.0.1:5000/store/some_name'
def get_store(name):
	pass

# GET /store
@app.route('/store')
def get_stores():
    # JSON is a dictionary, but stores is a list
    # 'http://127.0.0.1:5000/store' can see the definiton of list, but JSON only use double quotes
	return jsonify({'stores': stores}) # convert stores variable to JSON

# POST /store/<string: name>/item {name: , price }
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
	pass


# GET /store/<string: name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
	pass


app.run(port = 5000)
