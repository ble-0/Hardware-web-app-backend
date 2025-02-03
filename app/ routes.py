

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import db, Supplier, Product, User

def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({'message': 'Welcome all!'}), 200

    @app.route('/api/products', methods=['GET'])
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

    @app.route('/api/products', methods=['POST'])
    @jwt_required()
    def add_product():
        user_id = get_jwt_identity()
        data = request.get_json()

        if not all(key in data for key in ['name', 'description', 'price', 'category', 'supplier_id']):
            return jsonify({"message": "Missing required fields"}), 400

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')
        supplier_id = data.get('supplier_id')

        supplier = Supplier.query.filter_by(id=supplier_id).first()
        if not supplier:
            return jsonify({"message": "Supplier not found"}), 404

        new_product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            supplier_id=supplier_id
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"}), 201

    @app.route('/login', methods=['POST'])
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

    @app.route('/register', methods=['POST'])
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