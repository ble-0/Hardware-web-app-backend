
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import db, Supplier, Product, User

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello, world!"})

@api_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'category': p.category,
            'supplier': p.supplier.name
        } for p in products])
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@api_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        if not all(key in data for key in ['name', 'description', 'price', 'category', 'supplier_id']):
            return jsonify({"message": "Missing required fields"}), 400

        supplier = Supplier.query.filter_by(id=data['supplier_id']).first()
        if not supplier:
            return jsonify({"message": "Supplier not found"}), 404

        new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            category=data['category'],
            supplier_id=data['supplier_id']
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome all!'}), 200