from flask import Flask, jsonify, request, render_template, session, redirect, url_for, send_from_directory
from functools import wraps
import uuid
import os
import bcrypt
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient("mongodb://db:27017")
dbI = client.imageDB
images = dbI.images
db = client.user_login_system


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


@app.route('/')
def home():
    return_images = images.find()

    products = []
    for i in return_images:
        products.append(i)

    return render_template("home.html", products=products)

@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    searchItem= request.form['input']
    products = []
    product_cat = []

    return_images = images.find()

    # By default and when searchItem is None all the products are visible
    for i in return_images:
        if i['quantity'] > 0 and i['discontinued'] is False:
            products.append(i["id"])
            if searchItem.lower() not in i["name"].lower():
                product_cat.append('HIDE')
            else:
                product_cat.append('SHOW')
    return jsonify({'result' : 'success', 'products' : products, 'category':product_cat})


@app.route('/dashboard/', methods=['POST', 'GET'])
@login_required
def dashboard():
    return_images = images.find()

    products = []
    for i in return_images:
        if i['quantity'] > 0 and i['discontinued'] is False:
            products.append(i)

    if session['logged_in'] == True and session['admin'] == True:
        return render_template("dashboard.html", products=products, username=session['username'], userbalance=session['userbalance'], sessionadmin=True)
    if session['logged_in'] == True:
        return render_template("dashboard.html", products=products, username=session['username'], userbalance=session['userbalance'])
    
    return redirect('/')

def load_data():
    image = ({
        "id": uuid.uuid4().hex,
        "name": "Watch",
        "file": "../static/images/watch.jpg",
        "quantity": 10,
        "price": 200,
        "discontinued": False,
        "tags": ["Fashion", "Utility", "Official"]
    }, {
        "id": uuid.uuid4().hex,
        "name": "Cup",
        "file": "../static/images/cup.jpg",
        "quantity": 15,
        "price": 20,
        "discontinued": False,
        "tags": ["Home", "Decor"]
    }, {
        "id": uuid.uuid4().hex,
        "name": "Camera Roll",
        "file": "../static/images/roll.jpg",
        "quantity": 25,
        "price": 18,
        "discontinued": False,
        "tags": ["Home", "Decor"]
    }, {
        "id": uuid.uuid4().hex,
        "name": "Office Desk",
        "file": "../static/images/desk.jpg",
        "quantity": 3,
        "price": 20,
        "discontinued": False,
        "tags": ["Home", "Decor", "Work"]
    }, {
        "id": uuid.uuid4().hex,
        "name": "Telephone",
        "file": "../static/images/telephone.jpg",
        "quantity": 9,
        "price": 30,
        "discontinued": False,
        "tags": ["Home", "Office"]
    }, {
        "id": uuid.uuid4().hex,
        "name": "Analog",
        "file": "../static/images/analog_watch.jpg",
        "quantity": 3,
        "price": 250,
        "discontinued": True,
        "tags": ["Fashion", "Utility", "Official"]
    }
    )
    images.insert_many(image)
    # images.insert_one(image2)

def createAdminUser():
    ADMIN_USERNAME='admin'
    ADMIN_PASSWORD='password'
    users = db.users
    users.insert_one({'name': ADMIN_USERNAME, 'password': ADMIN_PASSWORD, 'userbalance': 500, 'products': {}})
