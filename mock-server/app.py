import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def load_data():
    with open('data/customers.json', 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/customers', methods=['GET'])
def get_customers():
    data = load_data()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    paginated_data = data[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_data,
        "total": len(data),
        "page": page,
        "limit": limit
    }), 200

@app.route('/api/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    data = load_data()
    for customer in data:
        if customer['customer_id'] == customer_id:
            return jsonify(customer), 200
    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
