from flask import Flask, request, render_template, redirect, url_for, jsonify
from auth import authenticate_user, register_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cryptography.fernet import Fernet

# Ideally save/load this from a secure place
KEY = Fernet.generate_key()
cipher = Fernet(KEY)
app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if authenticate_user(username, password):
            return f"<h2>Welcome, {username}!</h2>"
        else:
            message = "Invalid credentials. Try again."
    return render_template("login.html", message=message)

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if register_user(username, password):
        return redirect(url_for("login"))
    else:
        return "Username already exists. Try a different one.", 409

@limiter.limit("5 per minute")
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if authenticate_user(username, password):
        return jsonify({"message": "Login successful", "user": username}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if register_user(username, password):
        return jsonify({"message": "Registration successful", "user": username}), 201
    else:
        return jsonify({"error": "Username already exists"}), 409

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "API is up and running"}), 200

if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))