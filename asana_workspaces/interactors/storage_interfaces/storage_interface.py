"""
Storage interface for workspace operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from asana_workspaces.models.workspace import Workspace


class StorageInterface(ABC):
    @abstractmethod
    def create_workspace(
        self,
        name: str,
        is_organization: bool = False
    ) -> Workspace:
        pass

    @abstractmethod
    def get_workspace(self, workspace_gid: str) -> Optional[Workspace]:
        pass

    @abstractmethod
    def get_workspaces(
        self,
        offset: int = 0,
        limit: int = 50
    ) -> List[Workspace]:
        pass

    @abstractmethod
    def update_workspace(
        self,
        workspace_gid: str,
        name: Optional[str] = None,
        is_organization: Optional[bool] = None
    ) -> Workspace:
        pass

    @abstractmethod
    def delete_workspace(self, workspace_gid: str) -> bool:
        pass
    
    @abstractmethod
    def add_user_to_workspace(
        self,
        workspace_gid: str,
        user_gid: str
    ):
        pass
    
    @abstractmethod
    def remove_user_from_workspace(
        self,
        workspace_gid: str,
        user_gid: str
    ) -> bool:
        pass
    
    @abstractmethod
    def get_workspace_events(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List:
        pass

