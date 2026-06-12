#!/usr/bin/env python3
"""Module that defines index-level routes for API v1, including status,
stats, unauthorized, and forbidden test endpoints."""
from flask import jsonify, abort

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Return a JSON status OK response to confirm the API is running."""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Return counts of all objects stored in the database."""
    from models.user import User
    stats = {'users': User.count()}
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> None:
    """Trigger a 401 Unauthorized error for testing the error handler."""
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> None:
    """Trigger a 403 Forbidden error for testing the error handler."""
    abort(403)
