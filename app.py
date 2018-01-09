# the server, the Flask application has to be created to understand requests from browsers

# tell Python we want to use flask
from flask import Flask

app = Flask(__name__) # create a Flask object with unique name 

# create a route for homepage
@app.route('/') # end-point with /
def home():
	# return a response to browsers
	return "Hello, world!"

app.run(port = 5000)