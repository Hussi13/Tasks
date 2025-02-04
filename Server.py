from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
import cv2
import base64
import numpy as np
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

cluster = MongoClient("mongodb+srv://HusseinDB:Od8qEQZvB9sBIwQI@cluster0.fhj27.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["HusseinDB"]
collection = db["users"]

MODEL = YOLO("best.pt")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

try:
    cluster.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB Connection Failed: {e}")

@app.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
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
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
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
        user["_id"] = str(user["_id"])
    return jsonify(users), 200

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

@app.route("/detect", methods=["POST"])
def detect_objects():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    image_file = request.files["image"]
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)
    results = MODEL(image_path, save=True)
    output_dir = "runs/detect/predict/"
    detected_image_path = os.path.join(output_dir, image_file.filename)
    if not os.path.exists(detected_image_path):
        return jsonify({"error": "Detection failed, output file not found"}), 500
    encoded_image = encode_image(detected_image_path)
    return jsonify({"image_base64": encoded_image, "message": "Detection successful!"})

@app.route("/")
def home():
    return "Welcome to Hussein's API!", 200

if __name__ == "__main__":
    app.run(debug=True)
