from typing import Dict, Any, List
from asana_attachments.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetAttachmentPresenterImplementation(PresenterInterface):
    def get_attachment_response(
        self,
        attachment_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': attachment_dict
        }

    def get_attachments_response(
        self,
        attachments_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': attachments_list
        }

