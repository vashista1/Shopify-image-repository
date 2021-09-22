from flask import Flask, request
from app import app,login_required
from inventory.shop import Shopping


@app.route("/buy/<productid>")
@login_required
def buyProduct(productid):
    return Shopping().buyProduct(productid)

@app.route("/sell/<productid>")
@login_required
def sellProduct(productid):
    return Shopping().sellProduct(productid)

@app.route('/dashboard/removeproducts/<productid>')
@login_required
def removeProduct(productid):
    return Shopping().removeProduct(productid)

@app.route('/dashboard/removeproducts')
@login_required
def removeProductPage():
    return Shopping().removeProductPage()

@app.route('/dashboard/addproductsnew', methods=['POST', 'GET'])
@login_required
def addProductsNew():
    return Shopping().addProductsNew(request.method)
    
@app.route('/dashboard/addproducts')
@login_required
def addProducts():
    return Shopping().addProducts()

@app.route('/dashboard/addproducts/<productid>')
@login_required
def addDiscontinuedProduct(productid):
    return Shopping().addDiscontinuedProduct(productid)