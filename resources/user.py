from typing import Optional

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'username',
            type=str,
            required=True,
            help="This field is required!"
        )
    parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This field is required!"
        )

    def post(self):
        data = UserRegister.parser.parse_args()
        print(data)

        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists"}, 400

        user = UserModel(**data)

        try:
            user.save_to_db()
        except:
            return {"message": "Error encountered trying to create user"}, 500
        else:
            return {"message": f"user {data['username']!r} created successfully"}, 201
