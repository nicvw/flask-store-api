from __future__ import annotations

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    base_parser = reqparse.RequestParser()
    base_parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs to be associated with a store!"
    )
    parser = base_parser.copy()
    parser.add_argument("price", type=float, required=True, help="Every item needs a price!")

    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message", "An error occured accessing the database"}, 500

        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name!r} and id {data['store_id']!r} already exists."}, 400

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message", "An error occured accessing the database"}, 500
        else:
            return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Admin privilige required"}, 401
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {"items": [x["name"] for x in items], "message": "Login to retrieve detailed item data"}, 200
