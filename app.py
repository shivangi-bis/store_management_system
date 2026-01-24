from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from database import get_connection
from models import add_product, get_all_products, update_product, delete_product
from auth import token_required  # your JWT token decorator if needed

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"  # change this in production
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# ------------------- HOME -------------------
@app.route("/")
def home():
    return jsonify({"message": "Store Management API running"})

# ------------------- REGISTER -------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "staff")  # default role is staff

    if not username or not password:
        return {"error": "Username and password required"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return {"error": "Username already exists"}, 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_password, role)
    )
    conn.commit()
    conn.close()

    return {"message": f"User {username} registered successfully!"}, 201

# ------------------- LOGIN -------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return {"error": "Invalid username or password"}, 401

    access_token = create_access_token(identity={"username": username, "role": user["role"]})
    return {"access_token": access_token}, 200

# ------------------- PRODUCT ROUTES -------------------

# GET all products (any logged-in user)
@app.route("/products", methods=["GET"])
#@jwt_required()
def list_products():
    products = get_all_products()
    result = []
    for p in products:
        result.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "quantity": p["quantity"]
        })
    return jsonify(result)

# ADD product (admin only)
@app.route("/products", methods=["POST"])
@jwt_required()
def add_new_product():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return {"error": "Admin access required"}, 403

    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or price is None or quantity is None:
        return {"error": "All product fields required"}, 400

    add_product(name, price, quantity)
    return {"message": f"Product {name} added successfully!"}, 201

# UPDATE product (admin only)
@app.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_existing_product(product_id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return {"error": "Admin access required"}, 403

    data = request.get_json()
    update_product(
        product_id,
        name=data.get("name"),
        price=data.get("price"),
        quantity=data.get("quantity")
    )
    return {"message": f"Product {product_id} updated successfully!"}

# DELETE product (admin only)
@app.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_existing_product(product_id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return {"error": "Admin access required"}, 403

    delete_product(product_id)
    return {"message": f"Product {product_id} deleted successfully!"}

# ------------------- RUN SERVER -------------------
if __name__ == "__main__":
    app.run(debug=True)
