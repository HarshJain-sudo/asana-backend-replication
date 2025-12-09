from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_project_response(
        self,
        project_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_projects_response(
        self,
        projects_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

