from flask import Flask, jsonify, request
from pymongo import MongoClient # type: ignore

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["my_records"]
orders_collection = db["orders"]

@app.get('/get-items')
def get_items():
   
    # Fetch orders and convert to list
    orders = list(orders_collection.find())
    # Convert ObjectId to string for JSON compatibility
    for order in orders:
        order["_id"] = str(order["_id"])

    return jsonify(orders)


@app.post("/add-order")
def add_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    if "order_id" not in data or "product" not in data or "c_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if orders_collection.find_one({"order_id": data["order_id"]}):
        return jsonify({"error": "Order ID already exists"}), 400
    # Insert into MongoDB
    result = orders_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)  # Include _id as string in response

    return jsonify({"message": "Order added", "order": data}), 201



