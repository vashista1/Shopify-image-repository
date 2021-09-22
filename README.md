# Shopify-image-repository

## Winter 2022 - Shopify

## Developer Intern Challenge Question

This a web application built using Docker, Flask, MongoDB technologies. This application is developed as part of [Shopify Internship Challenge Winter 2022](https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit)

This application mimics an e-commerce store with front-end where the users could purchase and sell their products. Addionally, admin users have the ability to add and remove products within the store using the front-end.

On the backend, the application is running on **Flask** with **MongoDB** as Database in a **Docker Envirornment**.

The test envirornment is also setup on a Docker container. Pre-defined test cases start running approximately 10-15 seconds after the Flask server is up. **Test reulsts can be monitored via terminal**

# Installation
Install Docker to access the application.

 `Docker` and `docker-compose` should be installed on your systemb to run this application. Please visit [here](https://docs.docker.com/engine/install/) to install `Docker` and [here](https://docs.docker.com/compose/install/) to install `docker-compose` .


Please visit [here](https://docs.docker.com/get-docker/) to find additional instructions on installing `Docker`.

After installation make sure Docker is up and running!

This method starts 

1. Download the repository [Shopify-image-repository](https://github.com/vashista1/Shopify-image-repository/archive/refs/heads/main.zip)
    (or) git clone:
    ```sh
    git clone https://github.com/vashista1/Shopify-image-repository.git
    ```

2. Navigate to the folder
    ```sh
    cd Shopify-image-repository
    ```
3. Run the following Docker Command to excute the application on your localhost on the port 5000:
    
    *This command starts up all three containers (Database, Web server and Testing):
    Pre-defined test cases will automatically run after the web-server is up, you can observe progress in terminal.*

    ```sh
    docker-compose up --build --force-recreate
    ```
    (or)
    
    *This command srtarts up only (Database and Web server) containers.*

    ```sh
    docker-compose -f docker-compose.prod.yml up
    ```

    **The web application will be running on [http://0.0.0.0:5000/](http://0.0.0.0:5000/) or [http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

Admin Credentials ([Login!](http://127.0.0.1:5000/login)): 

Username/Password:(**admin**/**admin**)



# Features
**The application has the following features:**

- Register a new user and make transactions **(Buy and Sell)** with default $500 balance.

    ![alt text](/images/user_signup.gif)
- Admin users can make transactions as regular users and have the ability to **Discontinue (Delete)** products from store and **Add** new and discontinued products to the store.

    ![alt text](/images/admin_user.gif)
- All users can **Search** for products in their dashboard



### Avaliable Pages
- Home: Default page all users are greated to
- Dashboard: Users can buy products in this page, only avlaible after login
- Profile: Users can check their purchases and sell items if needed
- Login: Allows users to login to their store
- Register: Allows users to register
- Add (Discontinued): Only accessible by Admin users and allows them to add back discontinued products
- Add (New product): Only accessible by Admin users and allows them to add new products the store
- Remove: Only accessible by Admin users and allows them to remove/discontinue products

# Troubleshoot

Please run this command if an **Error running docker container. No space left on device** occurs.

```sh
docker volume rm $(docker volume ls -qf dangling=true)
```
