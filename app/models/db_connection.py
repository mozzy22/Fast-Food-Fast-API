import psycopg2
from urllib.parse import urlparse
import os

class DbConn :



    def create_connection(self):
        "A function to set up database connection"
        "A function to set up database connection"
        # self.conn = None
        try:
            if os.getenv('APP') == "testing":
                self.conn = psycopg2.connect(database="fast_food_test", user="postgres", password="moses",
                                             host="127.0.0.1",port="5432")

                return self.conn

            elif os.getenv('FLASK_ENV') == "heroku":

                url = "postgres://bqpdlaosdiimxb:bd0d1d8e01750838c6c97bad019f507eceac47bfd1dc4ea92693ea62318e4900@ec2-54" \
                      "-243-54-6.compute-1.amazonaws.com:5432/daf8s092fehhf3"

                parsed_url = urlparse(url)
                db = parsed_url.path[1:]
                username = parsed_url.username
                hostname = parsed_url.hostname
                password = parsed_url.password
                port = parsed_url.port

                self.conn = psycopg2.connect(
                    database=db, user=username, password=password,
                    host=hostname, port=port
                )
                return self.conn
            self.conn = psycopg2.connect(database="fast_food", user="postgres", password="moses",
                                         host="127.0.0.1", port="5432")

            return self.conn

        except Exception :
            print("Dtabase connection error ")
    def create_users_table(self):
        "A function to create the users_table"
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Users
              (user_id  SERIAL PRIMARY KEY  NOT NULL  ,
              first_name   TEXT   NOT NULL ,
              last_name  TEXT NOT NULL ,
              user_name  TEXT NOT NULL UNIQUE ,
               email     TEXT NOT NULL UNIQUE ,
               password   TEXT NOT NULL,
               created_at  DATE NOT NULL ,
               admin BOOLEAN NOT NULL
                ); ''')
        # print("Table users created successfully")
        self.conn.commit()

    def create_menu_table(self):
        "A function to create the menu table"
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Menu
                     (food_id  SERIAL PRIMARY KEY    NOT NULL ,
                      food_name    TEXT    NOT NULL UNIQUE,
                      food_price  MONEY NOT NULL
                      ); ''')
        # print("Table menu created successfully")
        self.conn.commit()


    def create_orders_table(self):
        "A function to create the orders table"
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS orders
                           (order_id  SERIAL PRIMARY KEY   NOT NULL ,
                            user_id    INT    references Users(user_id) NOT NULL,
                            food_id   INT     references Menu(food_id) NOT NULL,
                            order_uuid   UUID NOT NULL ,
                            created_at  TEXT NOT NULL ,
                            status   TEXT   NOT NULL ,
                            quantity INT NOT NULL
                             ); ''')
        # print("Table orders created successfully")
        self.conn.commit()
    def close_DB(self):

        self.conn.close()

con = DbConn()
con.create_connection()
con.create_users_table()
con.create_menu_table()
con.create_orders_table()
con.close_DB()