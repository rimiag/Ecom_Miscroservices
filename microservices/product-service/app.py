from flask import Flask, jsonify, request
from typing import Dict, Any

app = Flask(__name__)

# Type-annotated mock database
products_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    2: {"id": 2, "name": "Smartphone", "price": 699.99, "stock": 15}
}

@app.route("/", methods=["GET"])
def home():
    """Root endpoint with service information"""
    return jsonify({
        "service": "Product Service",
        "status": "running",
        "endpoints": {
            "list_products": "/products",
            "get_product": "/products/<id>"
        }
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route("/products", methods=["GET"])
def list_products():
    """List all products"""
    return jsonify(products_db)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    """Get a specific product by ID"""
    product = products_db.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route("/products", methods=["POST"])
def create_product():
    """Create a new product"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Input validation
    required_fields = {"name", "price"}
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        new_id = max(products_db.keys()) + 1
        products_db[new_id] = {
            "id": new_id,
            "name": data["name"],
            "price": float(data["price"]),
            "stock": data.get("stock", 0)
        }
        return jsonify(products_db[new_id]), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": "Invalid price value"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)