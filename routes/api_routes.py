
# routes/api_routes.py
from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return "Hello, API!"


    