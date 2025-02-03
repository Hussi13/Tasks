from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)


cluster = MongoClient("mongodb+srv://HusseinDB:Od8qEQZvB9sBIwQI@cluster0.fhj27.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["HusseinDB"]  
collection = db["users"]  


try:
    cluster.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")


@app.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    if not data or "First Name" not in data or "Last Name" not in data or "Email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    result = collection.insert_one(data)
    return jsonify({"message": "User created", "user_id": str(result.inserted_id)}), 201


@app.route("/create-all", methods=["POST"])
def create_all_users():
    data = request.get_json()

    
    if not isinstance(data, list):
        return jsonify({"error": "Input should be a list of user objects"}), 400

    result = collection.insert_many(data)
    return jsonify({"message": f"{len(result.inserted_ids)} users added"}), 201

@app.route("/delete/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200


@app.route("/delete-all", methods=["DELETE"])
def delete_all_users():
    result = collection.delete_many({})
    return jsonify({"message": f"{result.deleted_count} users deleted"}), 200

@app.route("/update/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    
    if not data or "First Name" not in data or "Last Name" not in data or "Email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated"}), 200

@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    user["_id"] = str(user["_id"])
    return jsonify(user), 200

@app.route("/get-all", methods=["GET"])
def get_all_users():
    users = list(collection.find({}))
    
    for user in users:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
    
    return jsonify(users), 200


@app.route("/")
def home():
    return "Welcome to the User Management API!", 200


if __name__ == "__main__":
    app.run(debug=True)
