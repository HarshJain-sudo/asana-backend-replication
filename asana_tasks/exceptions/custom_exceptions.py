from asana_tasks.constants.exception_messages import (
    TASK_DOES_NOT_EXIST,
    INVALID_TASK_GID,
)


class TaskDoesNotExistException(Exception):
    def __init__(self, message=TASK_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidTaskGidException(Exception):
    def __init__(self, message=INVALID_TASK_GID):
        self.message = message
        super().__init__(self.message)

