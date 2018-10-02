
class Config():
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = "mozzy"

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    # DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fast_food_test'
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fast_food'
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}