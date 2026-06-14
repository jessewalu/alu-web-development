#!/usr/bin/env python3
"""Module for Auth class that serves as the base authentication template."""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """Base class for all authentication mechanisms in the API."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required for the given path.

        Returns True if the path is not in excluded_paths, False otherwise.
        Slash-tolerant: /api/v1/status and /api/v1/status/ are treated equally.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Normalize path to always end with /
        normalized = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            if normalized == excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the Authorization header from the request.

        Returns None if the request is None or the header is absent.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user associated with the request.

        Always returns None in the base implementation.
        """
        return None

    def session_cookie(self, request=None):
        """Return the value of the session cookie from the request.

        Returns None if request is None. The cookie name is defined by the
        SESSION_NAME environment variable.
        """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
