from asana_attachments.constants.exception_messages import (
    ATTACHMENT_DOES_NOT_EXIST,
    INVALID_ATTACHMENT_GID,
)


class AttachmentDoesNotExistException(Exception):
    def __init__(self, message=ATTACHMENT_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidAttachmentGidException(Exception):
    def __init__(self, message=INVALID_ATTACHMENT_GID):
        self.message = message
        super().__init__(self.message)

