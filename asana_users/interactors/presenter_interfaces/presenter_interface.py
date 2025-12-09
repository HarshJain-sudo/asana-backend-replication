"""
Presenter interface for user responses.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_user_response(
        self,
        user_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_users_response(
        self,
        users_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass
