"""
Custom exceptions for asana_workspaces app.
"""
from asana_workspaces.constants.exception_messages import (
    WORKSPACE_DOES_NOT_EXIST,
    INVALID_WORKSPACE_GID,
)


class WorkspaceDoesNotExistException(Exception):
    def __init__(self, message=WORKSPACE_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidWorkspaceGidException(Exception):
    def __init__(self, message=INVALID_WORKSPACE_GID):
        self.message = message
        super().__init__(self.message)

