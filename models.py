

# from .extensions import db
# from werkzeug.security import generate_password_hash, check_password_hash


# # Suppliers Table
# class Supplier(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     contact_info = db.Column(db.String(200), nullable=True)

#     def __repr__(self):
#         return f'<Supplier {self.name}>'

# # Products Table
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(255), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     category = db.Column(db.String(100), nullable=False)
#     supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
#     supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))

#     def __repr__(self):
#         return f'<Product {self.name}>'

# # Users Table
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'

#     # Method to set password hash
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     # Method to check password
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(15), unique=True)  
    password = db.Column(db.Text(), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self, username, email, phone_number):
        self.username = username
        self.email = email
        self.phone_number = phone_number        
        db.session.commit()

# Hardware model
class Hardware(db.Model):  # Changed class name to Hardware for convention
    __tablename__ = "hardwares"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=True)

    def delete(self):
        db.session.delete(self)
        
    def save(self):
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        db.session.add(self)
        db.session.commit()  
        db.session.refresh(self)

    def update(self, name=None, quantity=None, supplier=None, location=None, last_restocked=None):
        try:
            if name and not isinstance(name, str):
                raise ValueError("Name must be a string.")
            if quantity is not None:
                if not isinstance(quantity, int) or quantity < 0:
                    raise ValueError("Quantity must be a non-negative integer.")
                self.quantity = quantity
            if supplier and not isinstance(supplier, str):
                raise ValueError("Supplier must be a string.")
            if location and not isinstance(location, str):
                raise ValueError("Location must be a string.")
            if last_restocked:
                if isinstance(last_restocked, str):
                    try:
                        last_restocked = datetime.strptime(last_restocked, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValueError("Date must be in the format 'YYYY-MM-DD'")
                self.last_restocked = last_restocked
            
            db.session.commit()
        except Exception as e:  # Changed to a generic Exception for better clarity
            db.session.rollback()
            raise e
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "destination": self.destination,
            "details": self.details,
            "date": self.date.isoformat() if self.date else None,
        }      
        
    def __repr__(self):
        return f'<Hardware {self.title}>'  # Changed to self.title for clarity
    
         
    
    
 
        