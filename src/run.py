from app import app, load_data, createAdminUser
import user.routes
import inventory.routes

if __name__ == "__main__":
    load_data()
    createAdminUser()
    app.run(host='0.0.0.0')