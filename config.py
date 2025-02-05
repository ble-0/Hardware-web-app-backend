

# class Config:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///hardware_order.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = 'your-secret-key'  # Change this to your secret key


import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    # Get database credentials
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost
    DB_PORT = os.getenv('DB_PORT', '5432')  # Default to 5432
    DB_NAME = os.getenv('DB_NAME')

    # Ensure all required environment variables are set
    if not DB_USER or not DB_PASSWORD or not DB_NAME:
        raise ValueError("Missing required database credentials (DB_USER, DB_PASSWORD, DB_NAME).")

    # Construct the DATABASE_URL correctly
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DEBUG = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_ECHO = False
    TESTING = True