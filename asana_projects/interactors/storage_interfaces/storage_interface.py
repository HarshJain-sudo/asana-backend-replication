from abc import ABC, abstractmethod
from typing import List, Optional
from asana_projects.models.project import Project


class StorageInterface(ABC):
    @abstractmethod
    def get_project(self, project_gid: str) -> Optional[Project]:
        pass

    @abstractmethod
    def get_projects(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        archived: Optional[bool] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Project]:
        pass

    @abstractmethod
    def get_workspace_projects(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Project]:
        pass

    @abstractmethod
    def create_project(self, name: str, workspace_gid: str, **kwargs) -> Project:
        pass

    @abstractmethod
    def update_project(self, project_gid: str, **update_data) -> Optional[Project]:
        pass

    @abstractmethod
    def delete_project(self, project_gid: str) -> bool:
        pass

    @abstractmethod
    def get_project_tasks(self, project_gid: str, offset: int, limit: int) -> List:
        pass

