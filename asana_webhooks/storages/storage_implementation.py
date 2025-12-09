from typing import List, Optional
from asana_webhooks.models.webhook import Webhook
from asana_webhooks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_webhook(self, webhook_gid: str) -> Optional[Webhook]:
        try:
            return Webhook.objects.get(gid=webhook_gid)
        except Webhook.DoesNotExist:
            return None

    def get_webhooks(
        self,
        resource: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Webhook]:
        queryset = Webhook.objects.all()

        if resource:
            queryset = queryset.filter(resource=resource)

        return list(queryset[offset:offset + limit])

