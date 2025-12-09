"""
Custom exceptions for asana_users app.
"""
from asana_users.constants.exception_messages import (
    USER_DOES_NOT_EXIST,
    INVALID_USER_GID,
    USER_NOT_AUTHENTICATED,
)


class UserDoesNotExistException(Exception):
    def __init__(self, message=USER_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidUserGidException(Exception):
    def __init__(self, message=INVALID_USER_GID):
        self.message = message
        super().__init__(self.message)


class UserNotAuthenticatedException(Exception):
    def __init__(self, message=USER_NOT_AUTHENTICATED):
        self.message = message
        super().__init__(self.message)

