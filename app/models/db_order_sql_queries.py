from app.models.db_connection import DbConn



class DbQueries():

    def __init__(self):
        self.conn = DbConn().create_connection()
        self.cur = self.conn.cursor()


    def insert_orders(self, user_id, food_id, order_uuid,created_at,  status, quantity):
        "a method to insert orders into the orders table"

        sql = """INSERT INTO orders ( user_id ,food_id, order_uuid,created_at,  status,  quantity )
                              VALUES ('{user_id}', '{food_id}', '{order_uuid}', '{created_at}', 
                              '{status}', '{quantity}' )"""

        sql_command = sql.format(user_id = user_id, food_id = food_id, order_uuid = order_uuid
                                 , created_at = created_at , status = status, quantity = quantity)
        self.cur.execute(sql_command)
        self.conn.commit()
        # self.conn.close()


    def get_orders(self, order_list = []):
        "a methos to fetch orders froorders table"
        order_list.clear()
        sql = """SELECT * FROM orders  ;"""
        self.cur.execute(sql)
        orders = self.cur.fetchall()
        order = {}
        for row in orders:
            order = {
                "order_id": row[0],
                "order_client": row[1],
                "order_food_id": row[2],
                "order_uuid": row[3],
                "order_created_at": row[4],
                "order_status": row[5],
                "order_quantity": row[6]
            }
            order_list.append(order)
        self.conn.commit()
        # self.conn.close()
        return order_list

    def fetch_order(self, uuid):
        "a methos to fetch specific order"
        sql = """SELECT * FROM orders WHERE order_uuid = '{uuid}' ;"""
        sql_command = sql.format(uuid = uuid)

        self.cur.execute(sql_command)
        orders = self.cur.fetchall()
        order = {}
        for row in orders:
            order = {
                "order_id": row[0],
                "order_client": row[1],
                "order_food_id": row[2],
                "order_uuid": row[3],
                "order_created_at": row[4],
                "order_status": row[5],
                "order_quantity": row[6]
            }
        self.conn.commit()
        # self.conn.close()
        return order

    def update_order_status(self, status ,uuid):
        "a methos to update order status"
        sql = """UPDATE orders  SET status = '{status}' WHERE order_uuid = '{uuid}';"""


        sql_command = sql.format(status = status,uuid = uuid)

        self.cur.execute(sql_command)
        self.conn.commit()
        # self.conn.close()


    def insert_food(self,food_name, food_price):
        "a methos to insert food object into menu tale"

        sql = """INSERT INTO menu ( food_name, food_price )  VALUES ('{food}', '{price}');"""
        sql_command = sql.format(food =food_name, price = food_price)
        self.cur.execute(sql_command)
        self.conn.commit()
        # self.conn.close()

    def get_food(self, food_name):
         "a methos to get food "
         sql =  """SELECT * FROM menu WHERE food_name = '{name}' ;"""
         sql_command = sql.format(name = food_name)
         self.cur.execute(sql_command)
         foods = self.cur.fetchall()
         food = {}

         for row in foods:
             food = {
             "food_id" : row[0],
             "food_name": row[1],
             "food_price" : row[2]
             }
         self.conn.commit()
         # self.conn.close()
         return food

    def get_all_foods(self, food_list = []):
        "a method to get all foods"
        food_list.clear()
        sql = """SELECT * FROM menu ;"""
        self.cur.execute(sql)
        foods = self.cur.fetchall()
        food = {}

        for row in foods:
            food = {
                "food_id": row[0],
                "food_name": row[1],
                "food_price":row[2]
            }
            food_list.append(food)
        self.conn.commit()
        # self.conn.close()
        return food_list

    def close_conn(self):
        DbConn().close_DB()


