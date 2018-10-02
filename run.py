from app.views.routes import My_app
from config.config import app_config
from app.models.db_connection import DbConn

My_app.config.from_object(app_config["development"])



if __name__ == "__main__":
    My_app.run()
