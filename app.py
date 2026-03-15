from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Allow frontend access
CORS(app)

# ================= MAIL CONFIG =================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "sowmiya02102004@gmail.com"
app.config['MAIL_PASSWORD'] = "alyh dmil urtn ujkl"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# ================= STORAGE =================

otp_storage = {}
reset_otp_storage = {}

# ================= HOME =================

@app.route("/")
def home():
    return "AyurSutra Backend is Running"

# ================= LOGIN =================

@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data.get("email")
    password = data.get("password")

    print("Login request:", email)

    msg = Message(
        subject="AyurSutra Login Notification",
        sender="sowmiya02102004@gmail.com",
        recipients=[email]
    )

    msg.body = f"""
You logged into AyurSutra.

Email: {email}
Password: {password}
"""

    try:
        mail.send(msg)
        return jsonify({"message": "Login successful and email sent"})
    except Exception as e:
        print("Mail error:", e)
        return jsonify({"message": "Login successful but email failed"})


# ================= SEND OTP =================

@app.route("/send-otp", methods=["POST"])
def send_otp():
    try:
        data = request.json
        email = data.get("email")

        otp = random.randint(100000, 999999)
        otp_storage[email] = otp

        print("Generated OTP:", otp)

        msg = Message(
            subject="AyurSutra OTP Verification",
            sender="sowmiya02102004@gmail.com",
            recipients=[email]
        )

        msg.body = f"""
Welcome to AyurSutra!

Your OTP for registration is: {otp}

Please enter this OTP to verify your account.
"""

        mail.send(msg)

        return jsonify({"message": "OTP sent successfully"})

    except Exception as e:
        print("MAIL ERROR:", e)
        return jsonify({"message": "Failed to send OTP"}), 500


# ================= VERIFY OTP =================

@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.json

    email = data.get("email")
    user_otp = int(data.get("otp"))

    if otp_storage.get(email) == user_otp:
        return jsonify({"message": "OTP verified successfully"})
    else:
        return jsonify({"message": "Invalid OTP"})


# ================= RESET OTP =================

@app.route("/send-reset-otp", methods=["POST"])
def send_reset_otp():

    data = request.json
    email = data.get("email")

    otp = random.randint(100000, 999999)
    reset_otp_storage[email] = otp

    msg = Message(
        subject="AyurSutra Password Reset OTP",
        sender="sowmiya02102004@gmail.com",
        recipients=[email]
    )

    msg.body = f"Your OTP for password reset is: {otp}"

    try:
        mail.send(msg)
        return jsonify({"message": "OTP sent"})
    except Exception as e:
        print("Mail error:", e)
        return jsonify({"message": "Failed to send OTP"}), 500


# ================= RUN SERVER =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
