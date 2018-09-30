from flask import  Blueprint, jsonify, request
from app.models.users import User
from app.views.menu_blueprint import order_obj

user_blue = Blueprint('user_b', __name__ )
user_obj = User()


@user_blue.route('/auth/signup', methods =['POST'])
def user_signup():
    new_user =request.json

    if not user_obj.validate_user_obj(new_user):
        return jsonify({"error": "ivalid user obj"})

    new_first_name  = new_user["first_name"]
    new_last_name = new_user["last_name"]
    new_user_name = new_user["user_name"]
    new_email = new_user["email"]
    new_password = new_user["password"]

    invalid_password =  user_obj.validate_password(new_password)
    invalid_input = order_obj.validate_input(new_user,["first_name","last_name","user_name","email", "password"],
                                           [],["first_name","last_name","user_name","email", "password"] )

    if invalid_input:
        return jsonify(invalid_input)
    if not user_obj.validate_email(new_email):
        return jsonify({"error": "invalid email"})

    if invalid_password:
        return jsonify(invalid_password)
    if user_obj.check_existing_user(new_user_name,new_email):
        return jsonify({"error": "user name or email already exists"})
    return jsonify(user_obj.add_user(new_first_name,new_last_name,new_user_name,new_email,new_password))
    # return jsonify(user_obj.users_list)