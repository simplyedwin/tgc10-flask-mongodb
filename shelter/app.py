from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

# to use ObjectId to access an item in mongo db
from bson.objectid import ObjectId

# To allow the use of .env file
load_dotenv()

app = Flask(__name__)

# this is to retrieve info/setting from .
# env file via the arg in os.environ.get()
MONGO_URI = os.environ.get('MONGO_URI')

DB_NAME = 'tgc10_new_shelter'
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/animals')
def show_all_animals():
    animals = db.animals.find()
    return render_template('show_animals.template.html',
                           htmlanimals=animals)


@app.route('/animals/create')
def show_create_animals():
    return render_template('create_animals.template.html')


@app.route('/animals/create', methods=['POST'])
def process_create_animals():
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = request.form.get('age')
    animal_type = request.form.get('type')

    # insert only ONE new document
    db.animals.insert_one(
        {
            "name": name,
            "age": age,
            "breed": breed,
            "type": animal_type
        }
    )

    return "New Animal Saved!"

# this route is to get the id to be deleted
# and prompt the user for confirmation


@app.route('/animals/<animal_id>/delete')
def delete_animal(animal_id):
    animal = db.animals.find_one(
        {
            "_id": ObjectId(animal_id)
        }
    )

    return render_template('confirm_delete_animal.template.html',
                           animal_to_delete=animal)


@app.route('/animals/<animal_id>/delete', methods=["POST"])
def process_delete_animal(animal_id):
    db.animals.remove({
        "_id": ObjectId(animal_id)
    })

    return redirect(url_for('show_all_animals'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'),
            debug=True)
