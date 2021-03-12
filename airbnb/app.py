from flask import Flask, render_template, request, redirect, url_for
import os
import random
import pymongo
from dotenv import load_dotenv

# To allow the use of .env file
load_dotenv()

app = Flask(__name__)

# this is to retrieve info/setting from .
# env file via the arg in os.environ.get()
MONGO_URI = os.environ.get('MONGO_URI')

DB_NAME = 'sample_airbnb'

# Create a MONGO client to connect to the DB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/')
def show_listings():
    listings = db.listingsAndReviews.find({},{
        'name':1,
        'summary':1
    }).limit(20)
    return render_template('listing.template.html', htmllistings=listings)


@app.route('/about-us')
def about():
    return '<h1>about-us<h1>'


@app.route('/lucky')
def luckyno():
    num = random.randint(1000, 9999)
    return 'Your lucky number is {}'.format(num)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
    # app.run(host='localhost', port=8080, debug=True)
