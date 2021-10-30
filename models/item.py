from __future__ import annotations

from typing import Dict, Optional

from db import db


class ItemModel(db.Model):
    __tablename__: str = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> Dict:
        return {
            "name": self.name,
            "price": self.price,
        }

    def enriched_json(self) -> Dict:
        return {"name": self.name, "price": self.price, "store": self.store.name}

    @classmethod
    def find(cls, name: str) -> Optional[ItemModel]:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
