from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# -----------------------------
# App Configuration
# -----------------------------
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

# -----------------------------
# Create Database
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------

# Add Product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    new_product = Product(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"}), 201


# Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])


# Update Product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data['name']
    product.price = data['price']
    product.quantity = data['quantity']

    db.session.commit()
    return jsonify({"message": "Product updated successfully"})


# Delete Product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"})


# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
