from app.views.routes import My_app
from config.config import app_config
from app.models.db_connection import DbConn

My_app.config.from_object(app_config["development"])



if __name__ == "__main__":
    db_obj = DbConn()
    con = db_obj.create_connection()
    db_obj.create_users_table()
    db_obj.create_menu_table()
    db_obj.create_orders_table()
    My_app.run()