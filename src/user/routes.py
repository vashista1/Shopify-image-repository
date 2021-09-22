from flask import Flask, request
from app import app,login_required
from user.models import User

@app.route('/register', methods=['POST', 'GET'])
def register():
    app.logger.info("here")
    return User().register(request.method)

@app.route('/login', methods=['POST', 'GET'])
def login():
    app.logger.info("hereLogin")
    return User().login(request.method)

@app.route('/signout')
@login_required
def signout():
    return User().signout()

@app.route('/profile')
@login_required
def profile():
    return User().profile()