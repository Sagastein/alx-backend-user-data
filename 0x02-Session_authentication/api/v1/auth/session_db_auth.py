#!/usr/bin/env python3
"""
Database Based session auth.
"""
from uuid import uuid4
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Database based session auth
    """
    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and returns the Session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())

        user_session = UserSession({'user_id': user_id,
                                    'session_id': session_id})

        user_session.save_to_file()

    def destroy_session(self, request=None):
        """
        Destory the session.
        """
        return super().destroy_session(request)
