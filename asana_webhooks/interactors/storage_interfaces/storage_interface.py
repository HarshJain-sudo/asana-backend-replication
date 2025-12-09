from abc import ABC, abstractmethod
from typing import List, Optional
from asana_webhooks.models.webhook import Webhook


class StorageInterface(ABC):
    @abstractmethod
    def get_webhook(self, webhook_gid: str) -> Optional[Webhook]:
        pass

    @abstractmethod
    def get_webhooks(
        self,
        resource: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Webhook]:
        pass

