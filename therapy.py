from flask import Blueprint, request, jsonify
from database import appointments

therapy_routes = Blueprint("therapy_routes", __name__)

@therapy_routes.route("/book-therapy", methods=["POST"])
def book_therapy():

    data = request.json

    booking = {
        "patient": data["name"],
        "therapy": data["therapy"],
        "date": data["date"]
    }

    appointments.insert_one(booking)

    return jsonify({"message":"Therapy booked successfully"})