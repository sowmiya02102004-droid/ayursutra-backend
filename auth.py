from flask import Blueprint, request, jsonify
from database import users

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.json

    user = {
        "name": data["name"],
        "email": data["email"],
        "mobile": data["mobile"],
        "password": data["password"]
    }

    users.insert_one(user)

    return jsonify({"message":"User registered successfully"})


@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.json

    user = users.find_one({
        "email":data["email"],
        "password":data["password"]
    })

    if user:
        return jsonify({"message":"Login successful"})
    else:
        return jsonify({"message":"Invalid credentials"})