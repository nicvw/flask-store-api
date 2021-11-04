from __future__ import annotations

from typing import Optional

from db import db


class UserModel(db.Model):
    __tablename__: str = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(102))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> Optional[UserModel]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, userid: int) -> Optional[UserModel]:
        return cls.query.filter_by(id=userid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def json(self):
        return {"id": self.id, "username": self.username}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
