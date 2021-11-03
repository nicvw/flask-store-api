from __future__ import annotations

from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {"message", "An error occured accessing the database"}, 500

        if store:
            return store.json()

        return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name!r} already exists."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message", "An error occured accessing the database"}, 500
        else:
            return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Item deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [x.json() for x in StoreModel.find_all()]}
