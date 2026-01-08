from flask import Flask, request, jsonify
from models import add_product, get_all_products, update_product, delete_product
from database import init_db

app = Flask(__name__)
init_db()  # Ensure DB is initialized

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    add_product(data['name'], data['price'], data['quantity'])
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products', methods=['GET'])
def read_products():
    products = get_all_products()
    result = [dict(p) for p in products]
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_products(product_id):
    data = request.get_json()
    update_product(product_id, data.get('name'), data.get('price'), data.get('quantity'))
    return jsonify({"message": "Product updated successfully!"})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_products(product_id):
    delete_product(product_id)
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
