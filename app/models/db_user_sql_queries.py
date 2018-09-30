from app.models.db_connection import DbConn

class UserQueries:

    def __init__(self):
        self.conn = DbConn().create_connection()
        self.cur = self.conn.cursor()


    def insert_user(self, first_name, last_name, user_name, email, password, created_at, admin):
          sql = """INSERT INTO  users ( first_name, last_name, user_name, email, password, created_at, admin )
                                     VALUES ('{f_name}', '{l_name}', '{u_name}', '{email}', '{password}',
                                     '{created_at}', '{admin}' )"""

          sql_command = sql.format(f_name = first_name, l_name = last_name, u_name = user_name, email = email
                                   ,password = password,  created_at = created_at, admin = admin )
          self.cur.execute(sql_command)
          self.conn.commit()
          # self.conn.close()


    def get_all_users(self, users_list = []):
        users_list.clear()
        sql = """SELECT * FROM users  ;"""
        self.cur.execute(sql)
        orders = self.cur.fetchall()
        user = {}
        for row in orders:
            user = {
                "user_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "user_name": row[3],
                "email": row[4],
                "password": row[5],
                "created_a": row[6],
                "admin": row[7]
            }
            users_list.append(user)
        self.conn.commit()
        # self.conn.close()
        return users_list

    def get_user(self, user_name):

        sql = """SELECT * FROM users WHERE  user_name ='{u_name}' ;"""
        sql_command = sql.format(u_name = user_name)
        self.cur.execute(sql_command)
        orders = self.cur.fetchall()
        user = {}
        for row in orders:
            user = {
                "user_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "user_name": row[3],
                "email": row[4],
                "password": row[5],
                "created_a": row[6],
                "admin": row[7]
            }
        self.conn.commit()
        # self.conn.close()
        return user

    def authorise_user(self, u_name, admin ):

        sql = """UPDATE users SET admin = '{admin}' WHERE user_name = '{u_name}';"""

        sql_command = sql.format(admin = admin , u_name = u_name)

        self.cur.execute(sql_command)
        self.conn.commit()
        # self.conn.close()

if __name__ == "__main__":
      db = UserQueries()
#     list = []
#     # print(db.get_user("mo"))
#     print(db.get_all_users(list))
#     # db.insert_user("moses","mutesasira", "mogg", "gmaiggl", "afafaf" , "12/11/11", True)

      db.authorise_user("mozzy", True)