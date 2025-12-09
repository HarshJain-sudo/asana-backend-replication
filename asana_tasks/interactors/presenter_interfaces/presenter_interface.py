from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_task_response(
        self,
        task_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_tasks_response(
        self,
        tasks_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_delete_response(self) -> Dict[str, Any]:
        pass

