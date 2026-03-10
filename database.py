from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ayursutra:VlyKexmDzySYlsgy@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["ayursutra"]

patients = db["patients"]
appointments = db["appointments"]
users = db["users"]