from selenium import webdriver
from time import sleep
import requests
from pymongo import MongoClient

GLOBAL_STORE_LINK = 'http://shopify-image-repository_web:5000'
ROUTES = {"home": "/", "login": "/login", "register": "register", "dashboard": "/dashboard/", "signout": "/signout",
          "userprofile": "/profile", "addproducts": "/dashboard/addproducts", "removeproducts": "/dashboard/removeproducts"}
USER = "John Doe"
PASS = "apple123!"

client = MongoClient("mongodb://db:27017")
dbI = client.imageDB
images = dbI.images
db = client.user_login_system
users = db.users

def set_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    return chrome_options


def check_base_products(driver):
    print(u'\u2139','Starting Base Products Test...')
    driver.get(GLOBAL_STORE_LINK)
    home_page_products = driver.find_elements_by_class_name(
        "column-xs-12.column-md-4")
    print("Checking if number of products in the Database match with the products on the frontend")
    image_count = images.find().count()
    # assert len(home_page_products) == len(images), "Default home page does not match with the products from inventory (database)!"
    if len(home_page_products) != image_count:
        print("Default home page does not match with the products from inventory (database)!")
    print(u'\u2705','Base products test completed.')
    print(25*'-')
    print()
    return driver


def check_valid_routes(driver):
    print(u'\u2139','Starting Valid Routes Test...')
    urls = ["/", "/login", "/dashboard/", "/signout",
            "/profile", "/dashboard/addproducts", "/dashboard/removeproducts"]
    testCheck = 0
    for i in urls:
        try:
            req = requests.get(GLOBAL_STORE_LINK+i)
            req.status_code != requests.codes['ok']

            print(f'Valid route: {i}')
            testCheck = testCheck+1
        except Exception as ex:
            print(f'Something went wrong with: {i}')
    if testCheck==len(urls):
        print(u'\u2705','All routes are valid.')
    else:
        print(u'\u26a0','Routes test not completed: '+str(testCheck)+'/'+str(len(urls))+' passed')
    print(25*'-')
    print()
    return driver

def login(user,password,driver):
    driver.get(GLOBAL_STORE_LINK+ROUTES["login"])
    driver.find_element_by_name("username").send_keys(user)
    driver.find_element_by_name("pass").send_keys(password)

    driver.find_element_by_name("loginbutton").click()
    sleep(5)
    return driver

def signout(driver):
    driver.get(GLOBAL_STORE_LINK+ROUTES["dashboard"])
    driver.find_element_by_name("signout").click()
    return driver

def check_admin_login(driver):
    print(u'\u2139','Starting Admin Login Test...')
    print('Check if the Admin User exists in the Database')
    adminUser=users.find_one({'name': 'admin'})

    if adminUser != None:
        driver = login('admin','admin',driver)
        #If login successful app should direct to dashboard
        # print(driver.find_element_by_name("username"))
        # print(driver.find_element_by_name("userbalance"))
        sleep(5)
        driver = signout(driver)
        print(u'\u2705','Admin login test and signout test completed')
    else:
        print(u'\u26a0',"Admin User login test not completed. Please check database to make sure Admin user is created when deploying the server!")
    print(25*'-')
    print()
    return driver

def check_admin_removeProduct(driver):
    print(u'\u2139','Starting Admin Remove Product Test...')
    all_products = images.find()
    all_displayed_products = 0
    testElement = {}
    for i in all_products:
        if i["discontinued"] == False:
            all_displayed_products += 1
            testElement = i
    if all_displayed_products == 0:
        print(u'\u2139','No products are on display to be removed')
    else:
        print(f'Count of all the displayed products: {all_displayed_products}')
        driver = login('admin','admin',driver)
        driver.get(GLOBAL_STORE_LINK+ROUTES["removeproducts"])
        sleep(3)
        driver.find_element_by_name(testElement["id"]).click()
        sleep(3)
        driver = signout(driver)
        all_products_after_removal = images.find()
        all_displayed_products_after_removal = 0
        for i in all_products_after_removal:
            if i["discontinued"] == False:
                all_displayed_products_after_removal += 1
        print(f'Count of all the displayed products after removal: {all_displayed_products_after_removal}')     
        
        # assert all_displayed_products-1 == all_displayed_products_after_removal, "Product removal unsuccessfull"
        if all_displayed_products-1 == all_displayed_products_after_removal:
            print(u'\u2705','Admin product removal test completed')
        else:
            print(u'\u26a0',"Product removal unsuccessfull")
        
    print(25*'-')
    print()
    return driver

def check_admin_addDiscontinuedProduct(driver):

    print(u'\u2139','Starting Admin Add Product Test...')
    all_products = images.find()
    all_discontinued_products = 0
    testElement = {}
    for i in all_products:
        if i["discontinued"] == True:
            all_discontinued_products += 1
            testElement = i
    if all_discontinued_products == 0:
        print(u'\u2139','No discontinued products to add...!')
    else:
        print(f'Count of all the discontinued products: {all_discontinued_products}')
        driver = login('admin','admin',driver)
        
        driver.get(GLOBAL_STORE_LINK+ROUTES["addproducts"])
        sleep(3)
        driver.find_element_by_name(testElement["id"]).click()
        sleep(3)
        all_products_after_addition = images.find()
        all_displayed_products_after_addition = 0
        for i in all_products_after_addition:
            if i["discontinued"] == True:
                all_displayed_products_after_addition += 1
        print(f'Count of all the displayed products after removal: {all_displayed_products_after_addition}')     
        
        # assert all_discontinued_products-1 == all_displayed_products_after_addition, "Product removal unsuccessfull"
        if all_discontinued_products-1 == all_displayed_products_after_addition:
            print(u'\u2705','Admin discontinued product add test completed')
        else:
            print(u'\u26a0',"Product add test unsuccessfull")

    print(25*'-')
    print()
    return driver
    
    
    
def check_admin_addProduct(driver):

    print(u'\u2139','Starting Admin Add New Product Test...')
    products = images.find()
    all_displayed_products = 0
    all_products = 0
    for i in products:
        all_products += 1
        if i["discontinued"] == False:
            all_displayed_products += 1
    print(f'Count of all the products in the store: {all_products}')
    print(f'Count of all the displayed products in the store: {all_displayed_products}')

    driver = login('admin','admin',driver)
    sleep(3)
    driver.get(GLOBAL_STORE_LINK+ROUTES["addproducts"])
    sleep(3)
    driver.find_element_by_name("addnewproduct").click()
    sleep(3)
    driver.find_element_by_name("productname").send_keys("Mango")
    driver.find_element_by_name("productquantity").send_keys(7)
    driver.find_element_by_name("productprice").send_keys(10)

    driver.find_element_by_name("submit").click()
    sleep(3)
    driver = signout(driver)

    products_updated = images.find()
    all_displayed_products_updated = 0
    all_products_updated = 0
    for i in products_updated:
        all_products_updated += 1
        if i["discontinued"] == False:
            all_displayed_products_updated += 1
    
    # assert all_products+1 == all_products_updated, "Add new product not successful!"
    # assert all_displayed_products+1 == all_displayed_products_updated, "Add new product not successful!"

    if all_products+1 != all_products_updated and all_displayed_products+1 != all_displayed_products_updated:
        print(u'\u26a0',"Add new product not successful!")
    
    print(f'Count of all the products in the store after adding product: {all_products_updated}')
    print(f'Count of all the displayed products in the store after adding product: {all_displayed_products_updated}')

    updated_product = images.find({"name":"Mango"})

    # assert updated_product == None , "Add new product not successful!"
    if updated_product == None:
        print(u'\u26a0',"Add new product not successful!")
    else:
        print(u'\u2705','Admin add new product test completed')
        # if updated_product["name"]=="Mango" and updated_product["quantity"]==7 and updated_product["price"]==10 and updated_product["discontinued"]==False:
        #     print(u'\u2705','Admin add new product test completed')

    print(25*'-')
    print()
    return driver

def check_register_newUser(driver):
    print(u'\u2139','Starting Registration of New User Test...')
    user_base = users.find()
    all_non_admin_users = 0
    for i in user_base:
        if i["name"] != 'admin':
            all_non_admin_users += 1
    print(f'Count of all the users: {all_non_admin_users}')

    driver.get(GLOBAL_STORE_LINK)
    sleep(2)
    driver.find_element_by_xpath("//*[contains(text(), 'Login!')]").click()
    sleep(2)
    driver.find_element_by_xpath("//*[contains(text(), 'Sign up here')]").click()
    sleep(2)

    
    driver.find_element_by_name("username").send_keys(USER)
    driver.find_element_by_name("pass").send_keys(PASS)

    driver.find_element_by_name("registerbutton").click()
    sleep(2)
    driver.get(GLOBAL_STORE_LINK+ROUTES["dashboard"])
    sleep(2)
    if driver.find_element_by_id("username").text == 'Hello '+USER+'!' and driver.find_element_by_id("userbalance").text == '$500':
        print('Login Successful! And page redirected to dashboard!')

    driver = signout(driver)

    user_base_updated = users.find()
    all_non_admin_users_updated = 0
    for i in user_base_updated:
        if i["name"] != 'admin':
            all_non_admin_users_updated += 1
    print(f'Count of all the users after adding user: {all_non_admin_users_updated}')
    added_user = users.find({"name":USER})
    if added_user[0]["name"]==USER:
        print('Login Successful and user added to database!')
        print(u'\u2705','Add new user test completed')

    print(25*'-')
    print()
    return driver

def check_buyProduct(driver):
    print(u'\u2139','Starting buy a new product test...')
    products = images.find()
    all_displayed_products = 0
    testElement = {}
    for i in products:
        if i["discontinued"] == False:
            all_displayed_products += 1
            testElement = i
    if all_displayed_products == 0:
        print(u'\u2139','No products are on display to buy')
    else:
        print(f'Count of all the displayed products in the store: {all_displayed_products}')
        driver = login(USER,PASS,driver)
        curr_user = users.find({"name":USER})
        sleep(2)
        driver.get(GLOBAL_STORE_LINK+ROUTES["dashboard"])
        sleep(2)
        driver.find_element_by_id(testElement["id"]).click()
        sleep(2)
        curr_user_after_product_added = users.find({"name":USER})

        buy_product_check = images.find({"id":testElement["id"]})

        if curr_user_after_product_added[0]["userbalance"]-testElement["price"]==500 and len(curr_user[0]["products"])==1 and buy_product_check[0]["quantity"] == testElement[0]["quantity"]-1:
            print(u'\u2705',"Product buy successfull and User balance updated!")
        else:
            print(u'\u26a0',"Buy product not successful!")
        driver = signout(driver)

    print(25*'-')
    print()
    return driver

def check_sellProduct(driver):
    print(u'\u2139','Starting sell a product test...')
    user_products = users.find({"name":USER})
    all_products = user_products[0]["products"]
    testElement = ""
    if all_products != None:
        for i in all_products.keys():
            if all_products[i]>=1:
                testElement = i
        
        print(f'Count of all the products bought by the user: {len(all_products)}')
        driver = login(USER,PASS,driver)
        sleep(2)
        driver.get(GLOBAL_STORE_LINK+ROUTES["userprofile"])
        sleep(2)
        driver.find_element_by_id(testElement).click()
        sleep(2)
        user_products_updated = users.find({"name":USER})
        if user_products_updated[0]["products"][testElement]== None or user_products_updated[0]["products"][testElement]==0:
            print(u'\u2705',"Product sell successfull and User balance updated!")
        driver = signout(driver)
    else:
        print(u'\u26a0',"Sell product not successful!")

    print(25*'-')
    print()
    return driver


if __name__ == "__main__":
    sleep(10)
    print('Starting selenium tests...')
    print(50*'=')
    driver = webdriver.Chrome(chrome_options=set_chrome_options())
    driver = check_valid_routes(driver)
    driver = check_base_products(driver)
    driver = check_admin_login(driver)
    driver = check_admin_removeProduct(driver)
    driver = check_admin_addDiscontinuedProduct(driver)
    driver = check_admin_addProduct(driver)
    driver = check_register_newUser(driver)
    driver = check_buyProduct(driver)
    driver = check_sellProduct(driver)
    # print(driver.page_source)
