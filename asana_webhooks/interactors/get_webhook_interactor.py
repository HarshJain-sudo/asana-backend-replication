from typing import Dict, Any
from asana_webhooks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_webhooks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_webhooks.exceptions.custom_exceptions import (
    WebhookDoesNotExistException
)


class GetWebhookInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_webhook(self, webhook_gid: str) -> Dict[str, Any]:
        webhook = self.storage.get_webhook(webhook_gid)

        if not webhook:
            raise WebhookDoesNotExistException()

        webhook_dict = {
            'gid': str(webhook.gid),
            'resource': webhook.resource,
            'resource_gid': webhook.resource_gid,
            'target': webhook.target,
            'active': webhook.active,
            'created_at': webhook.created_at.isoformat(),
            'updated_at': webhook.updated_at.isoformat(),
        }

        return self.presenter.get_webhook_response(webhook_dict)

