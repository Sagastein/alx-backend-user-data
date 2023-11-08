#!/usr/bin/env python3
"""
Basic Auth module.
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Basic Auth method
    """
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None \
           or not isinstance(authorization_header, str) \
           or not authorization_header.startswith('Basic '):
            return None

        return " ".join(authorization_header.split(' ')[1:])

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        try:
            base64_bytes = base64_authorization_header.encode("utf-8")

            base64_string_bytes = base64.b64decode(base64_bytes)

            return base64_string_bytes.decode("utf-8")

        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or \
           not isinstance(decoded_base64_authorization_header, str) or \
           ':' not in decoded_base64_authorization_header:
            return None, None

        pos = decoded_base64_authorization_header.find(':')

        email = decoded_base64_authorization_header[:pos]
        password = decoded_base64_authorization_header[pos + 1:]

        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str) \
            or user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrive current user.
        """
        authorization_header = self.authorization_header(request)

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)

        decoded_base64_authorization_header = self.decode_base64_authorization_header(
            base64_authorization_header)

        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_authorization_header)

        return self.user_object_from_credentials(user_email, user_pwd)
