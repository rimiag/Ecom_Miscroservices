from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Payment Service",
        "status": "running",
        "endpoint": "/payments/process (POST)"
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/payments/process", methods=["POST"])
def process_payment():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Input validation
    if "amount" not in data:
        return jsonify({"error": "Amount is required"}), 400
    
    # Mock payment processing
    return jsonify({
        "transaction_id": f"txn_{hash(data)}"[:20],
        "amount": data["amount"],
        "currency": data.get("currency", "USD"),
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003, debug=True)