from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_story_response(
        self,
        story_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_stories_response(
        self,
        stories_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

