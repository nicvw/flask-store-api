import os

from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse

from auth import authenticate, identity
from db import db
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
database_uri = os.getenv("DATABASE_URL", "sqlite:///data.db").replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = "123qwe"


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api = Api(app=app)
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
