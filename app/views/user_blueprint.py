from functools import wraps
import jwt
from app.models.orders import Orders
from app.models.users import User
from app.models. db_user_sql_queries import UserQueries
from flasgger import swag_from
from flask import Blueprint, jsonify, request, current_app
from flask import redirect

user_blue = Blueprint('user_b', __name__ )
user_obj = User()
order_obj = Orders()
querry = UserQueries()


@user_blue.route('/api/v1/auth/signup', methods =['POST'])
@swag_from('../docs/signup.yml')
def user_signup():
    " a function to signp user"
    new_user =request.json

    #validating user object
    if not user_obj.validate_user_obj(new_user):
        return jsonify({"error": "ivalid user obj"}), 400

    new_first_name  = new_user["first_name"]
    new_last_name = new_user["last_name"]
    new_user_name = new_user["user_name"]
    new_email = new_user["email"]
    new_password = new_user["password"]

    invalid_password =  user_obj.validate_password(new_password)
    invalid_input = order_obj.validate_input(new_user,["first_name","last_name","user_name","email", "password"],
                                           [],["first_name","last_name","user_name","email", "password"]
                                             ,["first_name","last_name","user_name"])
    #validating input
    if invalid_input:
        return jsonify(invalid_input), 400

    #validating email
    if not user_obj.validate_email(new_email):
        return jsonify({"error": "invalid email"}), 400

    # validating pasword
    if invalid_password:
        return jsonify(invalid_password), 400

    # check for existing user
    if user_obj.check_existing_user(new_user_name,new_email):
        return jsonify({"error": "user name or email already exists"}), 409

    #register user and return his details
    return jsonify(user_obj.add_user(new_first_name,new_last_name,new_user_name,new_email,new_password)), 201
    # return jsonify(user_obj.users_list)

@user_blue.route('/api/v1/auth/login', methods = ["POST"])
@swag_from('../docs/login.yml')
def login():
      " a function to login user"
      login_input = request.json
      if not user_obj.validate_login_obj( login_input):
           return jsonify({"error":"invalid login object"}), 400

      # getiing the user name
      user_name = login_input["user_name"]
      user_password = login_input["password"]
      invalid_input = order_obj.validate_input(login_input, ["user_name","password"], [], ["user_name","password"],["user_name"])

      #validating user input
      if invalid_input:
          return jsonify(invalid_input), 400

      validate_login_user = user_obj.validate_login_user(user_name,user_password)

      # validating user credentials
      if not validate_login_user:
          return jsonify({"error":"invalid login credentials"}), 401

      #generating tocken
      token = user_obj.generate_auth_token(validate_login_user["user_id"])
      return jsonify({"token": token}) ,200


@user_blue.route("/")
def main():
    return redirect("apidocs/")

def token_required(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        token = None

         # search for token in headers
        if "acces-token" in request.headers:
            token = request.headers["acces-token"]

        if not token:
            return jsonify({"error": "missing token"}), 401

         #extract user id
        try :
            data = jwt.decode(token, current_app.config.get('SECRET_KEY') )
            current_user =  data["user_id"]


        except:
            return jsonify({"error": "invalid token"}), 401

         # return decorated function with user id
        return func(current_user, *args, **kwargs)
    return authenticate



