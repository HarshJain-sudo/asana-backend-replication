from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_tag_response(
        self,
        tag_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_tags_response(
        self,
        tags_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

