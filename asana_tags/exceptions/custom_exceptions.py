from asana_tags.constants.exception_messages import (
    TAG_DOES_NOT_EXIST,
    INVALID_TAG_GID,
)


class TagDoesNotExistException(Exception):
    def __init__(self, message=TAG_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidTagGidException(Exception):
    def __init__(self, message=INVALID_TAG_GID):
        self.message = message
        super().__init__(self.message)


class WorkspaceDoesNotExistException(Exception):
    def __init__(self, message="Workspace does not exist"):
        self.message = message
        super().__init__(self.message)


class TagAlreadyExistsException(Exception):
    def __init__(self, message="Tag with this name already exists in workspace"):
        self.message = message
        super().__init__(self.message)

