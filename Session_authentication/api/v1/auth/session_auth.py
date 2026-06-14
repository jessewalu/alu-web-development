#!/usr/bin/env python3
"""Module for SessionAuth class implementing Session-based authentication."""
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """SessionAuth handles Session ID based authentication for the API."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create and store a new Session ID for the given user_id.

        Returns None if user_id is None or not a string, otherwise returns
        the newly generated Session ID.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the User ID associated with the given Session ID.

        Returns None if session_id is None, not a string, or not found.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return User instance associated with the request's session cookie.

        Uses session_cookie and user_id_for_session_id to determine User ID,
        then retrieves the corresponding User instance from the database.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session associated with the request (logout).

        Returns False if request is None, no session cookie is present, or
        the Session ID is not linked to any User ID. Otherwise deletes the
        session and returns True.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
