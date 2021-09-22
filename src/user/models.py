from flask import request,session, redirect, render_template
from app import db, images
import bcrypt
import uuid

class User:
    def start_session(self,user):
        session.clear()
        session['username'] = user['name']
        session['userbalance'] = user['userbalance']
        session['logged_in'] = True
        session['products'] = user['products']
        session['admin'] = False
        if user['name'] == 'admin':
            session['admin'] = True
        

    def register(self, method = 'GET'):
        if method == 'POST':
            users = db.users
            existing_user = users.find_one({'name': request.form['username']})

            if (existing_user == None) and (request.form['username'] != 'Admin'):
                salt = bcrypt.gensalt()
                # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), salt)
                users.insert_one({'name': request.form['username'], 'password': hashpass, 'userbalance': 500, 'products': {}})
                self.start_session({'name': request.form['username'], 'password': hashpass, 'userbalance': 500, 'products': {}})
                return redirect('/dashboard/')
            return render_template('register.html', alert="Username already exists. Please try again!")
        return render_template('register.html')
    
    def login(self, method = 'GET'):
        if method == 'POST':
            users = db.users
            login_user = users.find_one({'name': request.form['username']})
            if request.form['username'] == 'admin' and request.form['pass'] == 'admin':
                self.start_session(login_user)
                return redirect('/dashboard/')
            
            hashpass = login_user["password"]

            if login_user != None and bcrypt.checkpw(request.form['pass'].encode('utf-8'), hashpass):
                self.start_session(login_user)
                return redirect('/dashboard/')

            return render_template('login.html', alert="Username or Password do not exists. Please try again!")
        return render_template('login.html')
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def profile(self):
        users = db.users
        return_images = images.find()
        buyer_products = users.find_one({'name': session['username']})['products']

        products = []
        for i in return_images:
            if i['id'] in buyer_products and buyer_products[i['id']] > 0:
                i['buyerQuantity'] = buyer_products[i['id']]
                products.append(i)

        return render_template("profile.html", products=products, username=session['username'], userbalance=session['userbalance'])


        