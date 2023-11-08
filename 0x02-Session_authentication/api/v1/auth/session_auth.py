#!/usr/bin/env python3
"""
Session Based Authentication.
"""
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Based Authentication object.
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())

        SessionAuth.user_id_by_session_id[session_id] = user_id

        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns current active user.
        """
        session_id = self.session_cookie(request)

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout.
        """

        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return False

        del SessionAuth.user_id_by_session_id[session_id]

        return True
