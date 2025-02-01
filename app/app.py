
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hardware_order.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Suppliers Table
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Supplier {self.name}>'

# Products Table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'

# Users Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    # Method to set password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.before_request
def before_request():
    db.create_all()
    # Do something before each request
    pass

# Sample API endpoint to get product information

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
        return jsonify({"error": str(e)}), 500
