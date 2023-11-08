#!/usr/bin/env python3
"""
Authentication Module
"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authentication module for the api.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if the end point is required to authenticate.
        """
        if not path or not excluded_paths:
            return True

        path_with_slash = path if path.endswith('/') else path + '/'

        if path_with_slash in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header.
        """
        if not request:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current active user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request.
        """
        if request is None:
            return None

        cookie_name = getenv('SESSION_NAME')

        return request.cookies.get(cookie_name)
