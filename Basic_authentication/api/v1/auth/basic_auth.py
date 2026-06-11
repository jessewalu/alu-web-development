#!/usr/bin/env python3
"""Module for the BasicAuth class implementing HTTP Basic Authentication."""
import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth handles HTTP Basic Authentication for the API."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64-encoded credentials from the Authorization header.

        Returns None if the header is missing, not a string, or not Basic auth.
        Otherwise returns the Base64 portion after 'Basic '.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode a Base64 string and return it as a UTF-8 string.

        Returns None if the input is None, not a string, or not valid Base64.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user email and password from a decoded Base64 credential string.

        Returns (None, None) if the input is invalid or missing a colon.
        Otherwise returns (email, password) split on the first colon.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return the User instance matching the given email and password.

        Returns None if credentials are invalid, user not found, or password
        does not match.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the authenticated User for the current request.

        Chains together header extraction, Base64 decoding, credential parsing,
        and user lookup to return the matching User instance or None.
        """
        header = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64)
        email, password = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, password)
