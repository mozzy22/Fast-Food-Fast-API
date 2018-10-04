import datetime
import re

import jwt
from app.models.db_user_sql_queries import UserQueries
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.user_name = ""
        self.email = ""
        self.password = ""
        self.created_at = None
        self.admin = False
        self.querry = UserQueries()
        self.user = {}
        self.users_list = []



    def validate_password(self, password):
        password_error = {}

        if len(password)< 6 :
            password_error = {"error" : "weak password. Password must be atleat 6 charactors long"}
            return password_error
        if not re.search('[0-9]', password):
            password_error ={"error" : "Weak password. Password should have atleast one integer"}
            return password_error
        return password_error

    def validate_email(self, email):
        "function to verify email"
        match = re.match('[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z])', email)

        if match == None:
            return False
        else:
            return True

    def add_user(self, first_name, last_name, user_name, email,pasword ):

        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email = email
        self.password = generate_password_hash(pasword, method="sha256")
        self.created_at = datetime.datetime.now()
        self.admin = False
        self.querry.insert_user(self.first_name,self.last_name, self.user_name, self.email,
                                self.password, self.created_at, self.admin)
        return self.querry.get_user(self.user_name)


    def validate_user_obj(self, user_obj):
        "A method to validate a food object"
        if ( "first_name" in user_obj and "last_name" in user_obj and "user_name" in user_obj
             and  "email" in user_obj and "password" in user_obj):
            return True
        return False

    def check_existing_user(self,user_name, email):
        "a method to check whethr a given order already exists"
        exist = False
        for user in self.querry.get_all_users(self.users_list):
            if user["user_name"] == user_name or user["email"] == email:
                exist = True
                break
            else:
                exist = False
        return exist

    def validate_login_obj(self, login_obj):
        "A method to validate a food object"
        if ("user_name" in login_obj and "password" in login_obj ):
            return True
        return False

    def validate_login_user(self, username, password):
         login_user = {}
         for user in self.querry.get_all_users(self.users_list):
             if user['user_name'] == username and check_password_hash(user["password"], password):
                 login_user =user
                 break;
             pass

         return login_user


    def generate_auth_token(self, user_id):

        payload = {
            #user name
            "user_id": user_id,

            #expiry ate of token
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30) }

        token = jwt.encode( payload, current_app.config.get('SECRET_KEY'),algorithm='HS256' )

        return token.decode('UTF-8')

