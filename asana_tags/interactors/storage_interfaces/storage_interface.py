from abc import ABC, abstractmethod
from typing import List, Optional
from asana_tags.models.tag import Tag


class StorageInterface(ABC):
    @abstractmethod
    def get_tag(self, tag_gid: str) -> Optional[Tag]:
        pass

    @abstractmethod
    def get_tags(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        pass

    @abstractmethod
    def get_workspace_tags(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        pass
    
    @abstractmethod
    def create_tag(
        self,
        name: str,
        workspace_gid: str,
        color: str = None,
        notes: str = None,
        **kwargs
    ) -> Tag:
        pass
    
    @abstractmethod
    def update_tag(
        self,
        tag_gid: str,
        name: str = None,
        color: str = None,
        notes: str = None,
        **kwargs
    ) -> Tag:
        pass
    
    @abstractmethod
    def delete_tag(
        self,
        tag_gid: str
    ) -> bool:
        pass
    
    @abstractmethod
    def get_task_tags(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        pass

