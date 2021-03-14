from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

# To allow the use of .env file
load_dotenv()

app = Flask(__name__)

# this is to retrieve info/setting from .
# env file via the arg in os.environ.get()
MONGO_URI = os.environ.get('MONGO_URI')

DB_NAME = 'tgc10_new_shelter'
client = pymongo.MongoClient(MONGO_URI)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
