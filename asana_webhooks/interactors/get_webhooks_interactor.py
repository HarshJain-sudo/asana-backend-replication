from typing import Dict, Any, Optional
from asana_webhooks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_webhooks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_webhooks.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetWebhooksInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_webhooks(
        self,
        resource: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        webhooks = self.storage.get_webhooks(
            resource=resource,
            offset=offset,
            limit=limit
        )

        webhooks_list = [
            {
                'gid': str(webhook.gid),
                'resource': webhook.resource,
                'resource_gid': webhook.resource_gid,
                'target': webhook.target,
                'active': webhook.active,
                'created_at': webhook.created_at.isoformat(),
                'updated_at': webhook.updated_at.isoformat(),
            }
            for webhook in webhooks
        ]

        return self.presenter.get_webhooks_response(webhooks_list)

