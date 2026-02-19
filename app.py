from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data["password"]

    missing = []

    # Length check
    if len(password) < 8:
        missing.append("Minimum 8 characters")

    # Uppercase check
    if not re.search(r"[A-Z]", password):
        missing.append("At least one uppercase letter")

    # Lowercase check
    if not re.search(r"[a-z]", password):
        missing.append("At least one lowercase letter")

    # Number check
    if not re.search(r"[0-9]", password):
        missing.append("At least one number")

    # Special character check
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        missing.append("At least one special character")

    # Decide strength based on missing criteria
    if len(missing) == 0:
        strength = "Strong"
        message = "Valid Password"
    elif len(missing) <= 2:
        strength = "Medium"
        message = "Missing: " + ", ".join(missing)
    else:
        strength = "Weak"
        message = "Missing: " + ", ".join(missing)

    return jsonify({
        "strength": strength,
        "message": message
    })

if __name__ == "__main__":
    app.run(debug=True)
