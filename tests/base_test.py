import unittest
import psycopg2
from app.views.routes import My_app
from config.config import app_config
from app.models.db_connection import DbConn
from app.models.db_user_sql_queries import UserQueries
from app.models.orders import Orders
import json


class BaseTestCase(unittest.TestCase):


    def setUp(self):
        My_app.config.from_object(app_config["testing"])
        self.app = My_app.test_client()
        self.db_obj = DbConn()
        self.con  = self.db_obj.create_connection()
        self.db_obj.create_users_table()
        self.db_obj.create_menu_table()
        self.db_obj.create_orders_table()
        self.querry = UserQueries()
        self.hostname = "http://localhost:5000/api/v1/"
        self.order_obj = Orders()

        self.new_user = {
            "first_name": "moses",
            "last_name": "mut",
            "user_name": "mo1",
            "email": "aa@gmail.com",
            "password": "uuuuu6uu"}

        self.resgistered_user = {
            "user_name": "mo1",
            "password": "uuuuu6uu"}



    def tearDown(self):
        cursor = self.con.cursor()
        cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        cursor.execute("DROP TABLE IF EXISTS menu CASCADE")
        cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
        self.con.commit()
        self.con.close()


    def register_user(self,new_user):

        return self.app.post(self.hostname + "auth/signup", data=json.dumps(new_user),
                  content_type='application/json')

    def login_user(self, user):
        return self.app.post(self.hostname + "auth/login", data=json.dumps(user),
                             content_type='application/json')


    def make_admin(self, user):
        self.querry.authorise_user(user, True)

    def post_food(self, food, token ):
        return self.app.post(self.hostname + "menu", data=json.dumps(food),
                      content_type='application/json', headers=({"acces-token": token}))

    def get_all_orders(self,token):
        return self.app.get(self.hostname + "orders",headers=({"acces-token": token}) )

    def post_order(self,order, token):
        return self.app.post(self.hostname + "users/orders", data=json.dumps(order),
                             content_type='application/json', headers=({"acces-token": token}))

    def fetch_specific_order(self, uuid, token):
        return self.app.get(self.hostname + "orders/" + str(uuid), headers=({"acces-token": token}))

    def update_status(self,status,uuid,token):
        return self.app.put(self.hostname + "orders/" + str(uuid), data=json.dumps(status),
                             content_type='application/json', headers=({"acces-token": token}))

    def get_user_order_history(self,token):
        return self.app.get(self.hostname + "users/orders", headers=({"acces-token": token}))

    def get_menu(self,token):
        return self.app.get(self.hostname + "menu", headers=({"acces-token": token}))









if __name__ == '__main__':
    unittest.main()
