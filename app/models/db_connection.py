import psycopg2

class DbConn :

    def create_connection(self):
        "A function to set up database connection"
        self.conn = psycopg2.connect(database = "fast_food", user = "moses", password = "moses", host = "127.0.0.1", port = "5432")
        return self.conn



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
               admin BOOLEAN 
                ); ''')
        print("Table users created successfully")


    def create_menu_table(self):
        "A function to create the users_table"
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Menu
                     (food_id  SERIAL PRIMARY KEY    NOT NULL ,
                      food_name    TEXT    NOT NULL UNIQUE,
                      food_price  MONEY NOT NULL
                      ); ''')
        print("Table menu created successfully")



    def create_orders_table(self):
        "A function to create the ticket table"
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS orders
                           (order_id  SERIAL PRIMARY KEY   NOT NULL ,
                            user_id    INT    references Users(user_id) NOT NULL,
                            food_id   INT     references Menu(food_id) NOT NULL,
                            order_uuid   UUID NOT NULL ,
                            created_at  DATE NOT NULL ,
                            status   TEXT   NOT NULL UNIQUE,
                            quantity INT NOT NULL
                             ); ''')
        print("Table orders created successfully")

    def close_DB(self):
        self.conn.commit()
        self.conn.close()

con = DbConn()
con.create_connection()
con.create_users_table()
con.create_menu_table()
con.create_orders_table()
con.close_DB()