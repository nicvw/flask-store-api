from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp

from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help="This field is required!")
_user_parser.add_argument("password", type=str, required=True, help="This field is required!")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "Username already exists"}, 400

        user = UserModel(**data)

        try:
            user.save_to_db()
        except:
            return {"message": "Error encountered trying to create user"}, 500
        else:
            return {"message": f"user {data['username']!r} created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            return {
                "access_token": create_access_token(identity=user.id, fresh=True),
                "refresh_token": create_refresh_token(user.id),
            }, 200

        return {"message": "Invalid credentials"}, 401


class UserList(Resource):
    def get(self):
        return {"users": [x.json() for x in UserModel.find_all()]}
