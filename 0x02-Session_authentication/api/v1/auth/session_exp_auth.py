#!/usr/bin/env python3
"""
Adds an expiration date on the session auth.
"""
import datetime
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Adds expiration duration future for the session auth.
    """
    def __init__(self) -> None:
        super().__init__()
        self.session_duration = 0

        try:
            duration = getenv('SESSION_DURATION')
            self.session_duration = int(duration)
        except Exception:
            pass

    def create_session(self, user_id: str = None) -> str:
        """
        Add expiration duration attribute
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {}

        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.datetime.now()

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Check for session expiration.
        """

        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')

        if created_at is None:
            return None

        duration = datetime.timedelta(seconds=self.session_duration)

        if created_at + duration < datetime.datetime.now():
            return None

        return session_dictionary.get('user_id')
