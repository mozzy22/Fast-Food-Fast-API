from flask import  Blueprint, jsonify, request, current_app
from app.models.users import User
from app.models.orders import Orders
from app.models.db_user_sql_queries import UserQueries
from functools import wraps
import jwt


user_blue = Blueprint('user_b', __name__ )
user_obj = User()
order_obj = Orders()
querry = UserQueries()


@user_blue.route('/api/v1/auth/signup', methods =['POST'])
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

@user_blue.route('/api/v1/auth/login', methods = ["POST"])
def login():
      login_input = request.json
      if not user_obj.validate_login_obj( login_input):
           return jsonify({"error":"invalid login object"})

      user_name = login_input["user_name"]
      user_password = login_input["password"]
      invalid_input = order_obj.validate_input(login_input, ["user_name","password"], [], ["user_name","password"])

      if invalid_input:
          return jsonify(invalid_input)

      validate_login_user = user_obj.validate_login_user(user_name,user_password)

      if not validate_login_user:
          return jsonify({"error":"invalid login credentials"})
      user = {"user_id": validate_login_user["user_id"],
              "user_name": validate_login_user["user_name"],
              "user_email": validate_login_user["email"]
              }
      token = user_obj.generate_auth_token(validate_login_user["user_name"])
      return jsonify({"token": token})



def token_required(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        token = None

        if "acces-token" in request.headers:
            token = request.headers["acces-token"]

        if not token:
            return jsonify({"error": "missing token"})

        try :
            data = jwt.decode(token, current_app.config.get('SECRET_KEY') )
            current_user =  querry.get_user(data["user_name"])

        except:
            return jsonify({"error": "invalid token"})

        return func(current_user, *args, **kwargs)
    return authenticate



