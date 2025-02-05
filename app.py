
# # from flask import Flask
# # from routes.api_routes import api_bp  # Import your Blueprint or routes

# # def create_app():
# #     app = Flask(__name__)

# #     # Register the Blueprint with a URL prefix
# #     app.register_blueprint(api_bp, url_prefix='/api')

# #     # Add a root route
# #     @app.route('/')
# #     def root():
# #         return "Welcome to the Hardware Web App!"

# #     return app

    

# import os
# from flask import Flask
# from flask_restx import Api
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv

# from config import DevConfig, ProdConfig  # Import configurations
# from models import User, Itinerary
# from exts import db
# from auth import auth_ns
# from itineraries import itinerary_ns

# # Load environment variables from .env file
# load_dotenv()

# def create_app():
#     app = Flask(__name__)

#     # Determine environment (dev or prod)
#     env = os.getenv("FLASK_ENV", "development")  # Default to 'development' if not set
#     if env == "production":
#         app.config.from_object(ProdConfig)
#     else:
#         app.config.from_object(DevConfig)

#     # Enable CORS
#     CORS(app)

#     # Initialize extensions
#     db.init_app(app)
#     Migrate(app, db)
#     JWTManager(app)

#     # Set up API documentation
#     api = Api(app, doc='/docs')
#     api.add_namespace(hardware_ns)
#     api.add_namespace(auth_ns)

#     # Shell context for Flask CLI
#     @app.shell_context_processor
#     def make_shell_context():
#         return {"db": db, "hardware": Hardware, "User": User}

#     return app

# # Create the Flask app using the appropriate configuration
# app = create_app()

# if __name__ == '__main__':
#     # Ensure the app runs on the appropriate host and port (useful for local dev)
#     app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

    



import os
import sys
from pathlib import Path
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from dotenv import load_dotenv

from config import DevConfig, ProdConfig
from models import User, Hardware
from extensions import db
from auth import auth_ns
from hardware import hardware_ns
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent))

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()  # Initialize the SQLAlchemy instance
migrate = Migrate()  # Initialize the Migrate instance

def create_app():
    app = Flask(__name__)

    # Determine environment (dev or prod)
    env = os.getenv("FLASK_ENV", "development")  # Default to 'development' if not set
    if env == "production":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize migrate with app and db
    # jwt.init_app(app)  # Ensure you have this line if you're using JWT

    # Set up API documentation
    api = Api(app, doc='/docs')
    api.add_namespace(auth_ns)
    api.add_namespace(hardware_ns)

    # Shell context for Flask CLI
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "User": User, "Hardware": Hardware}  # Corrected 'hardware' to 'Hardware'

    return app

# Create the Flask app using the appropriate configuration
app = create_app()

if __name__ == "__main__":
    # Ensure the app runs on the appropriate host and port (useful for local dev)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

print("Initializing app module")