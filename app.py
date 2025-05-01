from flask import Flask, request, render_template, redirect, url_for
from auth import authenticate_user, register_user

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)