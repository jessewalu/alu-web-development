#!/usr/bin/env python3
"""Module that defines the Flask app for the user authentication service."""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
      - a JSON welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """ POST /users
    Form data:
      - email
      - password
    Register a new user.
    Return:
      - JSON payload with the registered email and a success message
      - 400 if the email is already registered
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Form data:
      - email
      - password
    Log in a user and create a new session.
    Return:
      - JSON payload with the email and a success message, with a
        session_id cookie set
      - 401 if the login credentials are invalid
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    Cookie:
      - session_id
    Log out a user by destroying their session.
    Return:
      - redirect to GET / on success
      - 403 if the session is invalid
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    Cookie:
      - session_id
    Return:
      - JSON payload with the user's email
      - 403 if the session is invalid
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
    Form data:
      - email
    Generate a reset password token for the user.
    Return:
      - JSON payload with the email and reset token
      - 403 if the email is not registered
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ PUT /reset_password
    Form data:
      - email
      - reset_token
      - new_password
    Update a user's password using a reset token.
    Return:
      - JSON payload with the email and a success message
      - 403 if the reset token is invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
