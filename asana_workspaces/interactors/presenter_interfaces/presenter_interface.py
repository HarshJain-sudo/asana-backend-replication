"""
Presenter interface for workspace responses.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_workspace_response(
        self,
        workspace_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_workspaces_response(
        self,
        workspaces_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_user_response(
        self,
        user_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

