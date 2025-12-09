from asana_webhooks.constants.exception_messages import (
    WEBHOOK_DOES_NOT_EXIST,
    INVALID_WEBHOOK_GID,
)


class WebhookDoesNotExistException(Exception):
    def __init__(self, message=WEBHOOK_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidWebhookGidException(Exception):
    def __init__(self, message=INVALID_WEBHOOK_GID):
        self.message = message
        super().__init__(self.message)

