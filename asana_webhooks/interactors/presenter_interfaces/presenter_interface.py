from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_webhook_response(
        self,
        webhook_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_webhooks_response(
        self,
        webhooks_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

