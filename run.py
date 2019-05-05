from config.config import app_config
from app.views.routes import My_app

My_app.config.from_object(app_config["development"])



if __name__ == "__main__":
    My_app.run()
