from flask import Blueprint, request, jsonify
from database import patients
from bson.objectid import ObjectId

patient_routes = Blueprint("patient_routes", __name__)


# ADD PATIENT
@patient_routes.route("/add-patient", methods=["POST"])
def add_patient():

    data = request.json

    patient = {
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "mobile": data["mobile"],
        "therapy": data["therapy"]
    }

    patients.insert_one(patient)

    return jsonify({"message": "Patient added successfully"})


# GET ALL PATIENTS
@patient_routes.route("/patients", methods=["GET"])
def get_patients():

    patient_list = []

    for patient in patients.find():

        patient["_id"] = str(patient["_id"])
        patient_list.append(patient)

    return jsonify(patient_list)


# GET SINGLE PATIENT
@patient_routes.route("/patient/<id>", methods=["GET"])
def get_patient(id):

    patient = patients.find_one({"_id": ObjectId(id)})

    patient["_id"] = str(patient["_id"])

    return jsonify(patient)


# DELETE PATIENT
@patient_routes.route("/delete-patient/<id>", methods=["DELETE"])
def delete_patient(id):

    patients.delete_one({"_id": ObjectId(id)})

    return jsonify({"message": "Patient deleted successfully"})