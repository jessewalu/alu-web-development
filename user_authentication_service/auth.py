#!/usr/bin/env python3
"""Module that defines the Auth class for the authentication service."""
import bcrypt
import uuid
from typing import Optional

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Return a salted, bcrypt-hashed version of the given password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize a new Auth instance with its own database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Raises ValueError if a user with the given email already exists.
        Otherwise returns the newly created User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Return True if the email/password combination is valid, else False."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                               user.hashed_password)

    def create_session(self, email: str) -> Optional[str]:
        """Create a new session for the user with the given email.

        Returns the new session ID, or None if no user with that email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Return the User associated with the given session ID, or None."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session associated with the given user_id."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate and store a reset password token for the given email.

        Raises ValueError if no user with the given email exists.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password using the given reset token.

        Raises ValueError if no user with the given reset token exists.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                              reset_token=None)
