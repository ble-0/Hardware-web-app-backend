
from flask import Flask
from routes.api_routes import api_bp  # Import your Blueprint or routes

def create_app():
    app = Flask(__name__)

    # Register the Blueprint with a URL prefix
    app.register_blueprint(api_bp, url_prefix='/api')

    # Add a root route
    @app.route('/')
    def root():
        return "Welcome to the Hardware Web App!"

    return app

    