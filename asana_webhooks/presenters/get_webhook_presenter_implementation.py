from typing import Dict, Any, List
from asana_webhooks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetWebhookPresenterImplementation(PresenterInterface):
    def get_webhook_response(
        self,
        webhook_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': webhook_dict
        }

    def get_webhooks_response(
        self,
        webhooks_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': webhooks_list
        }

