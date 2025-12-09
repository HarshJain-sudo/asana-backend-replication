from asana_projects.constants.exception_messages import (
    PROJECT_DOES_NOT_EXIST,
    INVALID_PROJECT_GID,
)


class ProjectDoesNotExistException(Exception):
    def __init__(self, message=PROJECT_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidProjectGidException(Exception):
    def __init__(self, message=INVALID_PROJECT_GID):
        self.message = message
        super().__init__(self.message)

