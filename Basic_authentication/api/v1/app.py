#!/usr/bin/env python3
"""Main Flask application module for API v1."""
import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Load the appropriate auth instance based on AUTH_TYPE env variable
auth = None
auth_type = os.getenv('AUTH_TYPE', '')

if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """Filter incoming requests: enforce authentication on protected routes."""
    if auth is None:
        return

    excluded = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
    ]

    if not auth.require_auth(request.path, excluded):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Return a JSON 401 Unauthorized response."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Return a JSON 403 Forbidden response."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """Return a JSON 404 Not Found response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
