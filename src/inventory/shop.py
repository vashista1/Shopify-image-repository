from flask import session, redirect, url_for, request, render_template
from app import db, images, app
import uuid
import os

class Shopping:
    def buyProduct(self,productid):
        users = db.users
        product_buyer = users.find_one({'name': session['username']})
        product = images.find_one({'id': productid})
        product_id = product['id']

        if product['quantity'] > 0 and (product_buyer['userbalance']-product['price']) >= 0:
            app.logger.info('Purchase can be made!')
            product_buyer['userbalance'] = product_buyer['userbalance'] - \
                product['price']
            if product_id in product_buyer['products']:
                product_buyer['products'][product_id] = product_buyer['products'][product_id] + 1
            else:
                product_buyer['products'][product_id] = 1

            session['userbalance'] = product_buyer['userbalance']
            session['products'] = product_buyer['products']
            users.update({'_id': product_buyer['_id']}, {'$set': product_buyer})

            app.logger.info('Deducted amount and updated personal cart')

            product['quantity'] = product['quantity']-1
            images.update({'_id': product['_id']}, {'$set': product})
            app.logger.info('Updated cart')

            return redirect(url_for('dashboard'))

        app.logger.info('An error occured please try again!')

        return ('', 204)

    def sellProduct(self,productid):
        users = db.users
        product_buyer = users.find_one({'name': session['username']})
        product = images.find_one({'id': productid})
        product_id = product['id']

        if product_id in product_buyer['products'] and product_buyer['products'][product_id] > 0:
            app.logger.info('Sale can be made!')
            product_buyer['userbalance'] = product_buyer['userbalance'] + \
                product['price']
            product_buyer['products'][product_id] = product_buyer['products'][product_id] - 1

            session['userbalance'] = product_buyer['userbalance']
            session['products'] = product_buyer['products']
            users.update({'_id': product_buyer['_id']}, {'$set': product_buyer})

            app.logger.info('Added to amount and updated personal cart')

            product['quantity'] = product['quantity']+1
            images.update({'_id': product['_id']}, {'$set': product})
            app.logger.info('Updated database')

            return redirect(url_for('profile'))

        app.logger.info('An error occured please try again!')

        return ('', 204)
    
    def addProductsNew(self,method):
        if session['admin'] == False:
            return ('',204)
        if method == 'POST':
            files = request.files.getlist("file")
            for file in files:
                productID = uuid.uuid4().hex
                productFile = str(productID)+file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], productFile))
                image = {
                    "id": productID,
                    "name": request.form['productname'],
                    "file": "../static/images/"+productFile,
                    "quantity": int(request.form['productquantity']),
                    "discontinued": False,
                    "price": int(request.form['productprice'])
                }
                images.insert_one(image)

            return redirect(url_for("dashboard"))
        return_images = images.find()

        products = []
        for i in return_images:
            if i['quantity'] > 0 and i['discontinued'] is True:
                products.append(i)
        return render_template("new_product.html", username=session['username'], userbalance=session['userbalance'])
    
    def removeProductPage(self):
        if session['admin'] == False:
            return ('',204)
        return_images = images.find()

        products = []
        for i in return_images:
            if i['discontinued'] is False:
                products.append(i)
        return render_template("remove.html", products=products, username=session['username'], userbalance=session['userbalance'])
    
    def addProducts(self):
        if session['admin'] == False:
            return ('',204)
        return_images = images.find()

        products = []
        for i in return_images:
            if i['discontinued'] is True:
                products.append(i)
        return render_template("add.html", products=products, username=session['username'], userbalance=session['userbalance'])

    def removeProduct(self,productid):
        if session['admin'] == False:
            return ('',204)
        product = images.find_one({'id': productid})
        product['discontinued'] = True
        images.update({'_id': product['_id']}, {'$set': product})
        app.logger.info('Updated cart')
        return redirect(url_for("removeProductPage"))
    
    def addDiscontinuedProduct(self,productid):
        if session['admin'] == False:
            return ('',204)
        product = images.find_one({'id': productid})
        product['discontinued'] = False
        images.update({'_id': product['_id']}, {'$set': product})
        app.logger.info('Updated cart')
        return redirect(url_for("addProducts"))


