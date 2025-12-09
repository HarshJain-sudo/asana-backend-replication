from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_attachment_response(
        self,
        attachment_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_attachments_response(
        self,
        attachments_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

