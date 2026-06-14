#!/usr/bin/env python3
"""Module that defines views for Session authentication routes."""
import os
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                  strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Form data:
      - email
      - password
    Return:
      - User object JSON represented with a session cookie set
      - 400 if email or password is missing
      - 404 if no user found for the given email
      - 401 if the password is wrong
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                  strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON dictionary with status code 200 on success
      - 404 if the session could not be destroyed
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
