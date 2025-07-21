from flask import Flask, jsonify, request
from pymongo import MongoClient # type: ignore

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["my_records"]
orders_collection = db["orders"]

@app.get('/get-items')
def get_items():
    orders = list(orders_collection.find())
    for order in orders:
        order["_id"] = str(order["_id"])

    return jsonify(orders)


@app.post("/add-order")
def add_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "order_id" not in data or "product" not in data or "c_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if orders_collection.find_one({"order_id": data["order_id"]}):
        return jsonify({"error": "Order ID already exists"}), 409
    
    # Insert into MongoDB
    result = orders_collection.insert_one(data)
    data["_id"] = str(result.inserted_id) 
    return jsonify({"message": "Order added", "order": data}), 201

@app.route('/update-order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # Find order
    existing_order = orders_collection.find_one({"order_id": order_id})
    if not existing_order:
        return jsonify({"message": f"No order found with order_id {order_id}"}), 404

    # Parse request JSON body
    data = request.get_json()
    update_data = {}

    # Optional fields
    if "product" in data and data["product"].strip():
        update_data["product"] = data["product"].strip()
    if "c_id" in data:
        try:
            update_data["c_id"] = int(data["c_id"])
        except ValueError:
            return jsonify({"message": "Invalid c_id"}), 400

    if not update_data:
        return jsonify({"message": "No valid fields to update"}), 400

    # Update in DB
    result = orders_collection.update_one({"order_id": order_id}, {"$set": update_data})
    if result.modified_count > 0:
        return jsonify({"message": f"Order {order_id} updated successfully"}), 200
    else:
        return jsonify({"message": "No changes made"}), 200

if __name__ == '__main__':
    app.run(debug=True)




