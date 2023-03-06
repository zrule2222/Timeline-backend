from flask import request
from flask_restplus import Resource, fields, Namespace
from sqlalchemy.sql import func
#from auth.views import LoginAPI

from models.User import UserModel
from schemas.User import UserSchema

USER_NOT_FOUND = "User not found."
USER_ALREADY_EXISTS = "User '{}' Already exists."


user_ns = Namespace('User', description='User related operations')
users_ns = Namespace('Users', description='Users related operations')

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

#Model required by flask_restplus for expect
user = user_ns.model('User', {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
})

class User(Resource):

    def get(self, id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message': USER_NOT_FOUND}, 404

    def delete(self,id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            user_data.delete_from_db()
            return {'message': "User Deleted successfully"}, 200
        return {'message': USER_NOT_FOUND}, 404

    @user_ns.expect(user)
    def put(self, id):
        user_data = UserModel.find_by_id(id)
        user_json = request.get_json();

        if user_data:
            user_data.username = user_json['username']
            user_data.email = user_json['email']
            user_data.password = user_json['password']
            user_data.updated_at = func.now()
        else:
            user_data = user_ns.load(user_json)

        user_data.save_to_db()
        return user_schema.dump(user_data), 200
    
class UserList(Resource):
    @user_ns.doc('Get all the Users')
    def get(self):
        return user_list_schema.dump(UserModel.find_all()), 200

    @user_ns.expect(user)
    @user_ns.doc('Create an user')
    def post(self):
        user_json = request.get_json()
        username = user_json['username']
        email = user_json['email']
        if UserModel.find_by_username(username):
            return {'message': USER_ALREADY_EXISTS.format(username)}, 400
        elif UserModel.find_by_email(email):
            return {'message': USER_ALREADY_EXISTS.format(email)}, 400
        user_data = user_schema.load(user_json)
        user_data.save_to_db()

        return user_schema.dump(user_data), 201