"""
Storage interface for user operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from asana_users.models.user import User


class StorageInterface(ABC):
    @abstractmethod
    def create_user(
        self,
        name: str,
        email: str,
        photo: Optional[str] = None
    ) -> User:
        pass

    @abstractmethod
    def get_user(self, user_gid: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_users(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[User]:
        pass

    @abstractmethod
    def update_user(
        self,
        user_gid: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        photo: Optional[str] = None
    ) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_gid: str) -> bool:
        pass

    @abstractmethod
    def get_user_workspaces(
        self,
        user_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List:
        pass
