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
    # if method is GET, use the below.else use
    # request.form.get for POST method
    # retrieve the value of the input named country
    country = request.args.get('country')
    min_beds = request.args.get('beds')
    page = request.args.get('page')
    page = request.args.get('page')

    # if page contains None, convert it to 0
    if page is None:
        page = 0
    else:
        # else convert the string to an integer
        page = int(page)

    criteria = {}
    if country:
        criteria['address.country'] = country

    if min_beds:
        criteria['beds'] = {
            "$gte": int(min_beds)
        }

    listings = db.listingsAndReviews.find(criteria, {
        'name': 1,
        'summary': 1,
        'images': 1,
        'address': 1,
        'beds': 1
    }).skip(page*20).limit(20)
    return render_template('listing.template.html',
                           htmllistings=listings, htmlpage=page,
                           htmlfullpath=request.full_path)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(
        os.environ.get('PORT')), debug=True)
    # app.run(host='localhost', port=8080, debug=True)
