
from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


def check_password_strength(password):
    """Evaluate password strength using basic rules."""

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add an uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add a lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add a number.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        feedback.append("Add a special character.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    if not feedback:
        feedback.append("Great! Your password meets all basic rules.")

    return {
        "strength": strength,
        "score": score,
        "feedback": feedback
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check-password", methods=["POST"])
def check_password():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")

    if not isinstance(password, str):
        return jsonify({"error": "Password must be text."}), 400

    if len(password) > 1024:
        return jsonify({"error": "Password is too long."}), 400

    result = check_password_strength(password)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
