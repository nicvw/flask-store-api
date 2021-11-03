import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from resources.item import Item, ItemList
from resources.user import User, UserLogin, UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
database_uri = os.getenv("DATABASE_URL", "sqlite:///data.db").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["PROPOGATE_EXCEPTION"] = True
app.secret_key = "123qwe"


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api = Api(app=app)
api.add_resource(UserLogin, "/auth")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
