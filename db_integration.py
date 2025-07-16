from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")


@app.get('/get-items')
def get_items():
   
    db = client["my_records"]
    orders_collection = db["orders"]

    # Fetch orders and convert to list
    orders = list(orders_collection.find())
    # Convert ObjectId to string for JSON compatibility
    for order in orders:
        order["_id"] = str(order["_id"])

    return jsonify(orders)

order33 = [
    {
        "order_id": 1115,
        "product": "screen",
        "c_id": 10041111
    },
    {
        "order_id": 885,
        "product": "charger",
        "c_id": 100425555
    }
]

@app.post('/add-items')
def add_items():
    data = request.get_json()
    
    if not all(k in data for k in ("order_id", "product", "c_id")):
        return jsonify({"error": "Missing fields"}), 400

    order33.append(data)
    return jsonify({"message": "Successfully added", "data": data}), 201
    # # Validate required fields
    # if not all(k in data for k in ("order_id", "product", "c_id")):
    #     return jsonify({"error": "Missing fields. Required: order_id, product, c_id"}), 400

    # # Insert into MongoDB
    # result = orders_collection.insert_one({
    #     "order_id": data["order_id"],
    #     "product": data["product"],
    #     "c_id": data["c_id"]
    # })

    # Correct 201 Created response
   # return jsonify({"message": "Item added", "id": str(result.inserted_id)}), 201





# if __name__ == '__main__':
#     app.run(debug=True)
