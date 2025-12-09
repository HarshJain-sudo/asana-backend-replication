from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from asana_tasks.models.task import Task


class StorageInterface(ABC):
    @abstractmethod
    def get_task(self, task_gid: str) -> Optional[Task]:
        pass

    @abstractmethod
    def get_tasks(
        self,
        workspace: Optional[str] = None,
        assignee: Optional[str] = None,
        project: Optional[str] = None,
        section: Optional[str] = None,
        completed_since: Optional[str] = None,
        modified_since: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Task]:
        pass

    @abstractmethod
    def create_task(
        self,
        name: str,
        workspace_gid: str,
        assignee_gid: Optional[str] = None,
        **kwargs
    ) -> Task:
        pass

    @abstractmethod
    def update_task(self, task_gid: str, **update_data) -> Optional[Task]:
        pass

    @abstractmethod
    def delete_task(self, task_gid: str) -> bool:
        pass

    @abstractmethod
    def add_project_to_task(self, task_gid: str, project_gid: str) -> Task:
        pass

    @abstractmethod
    def remove_project_from_task(self, task_gid: str, project_gid: str) -> Task:
        pass

    @abstractmethod
    def add_tag_to_task(self, task_gid: str, tag_gid: str) -> Task:
        pass

    @abstractmethod
    def remove_tag_from_task(self, task_gid: str, tag_gid: str) -> Task:
        pass

    @abstractmethod
    def add_followers_to_task(self, task_gid: str, follower_gids: List[str]) -> Task:
        pass

    @abstractmethod
    def remove_followers_from_task(self, task_gid: str, follower_gids: List[str]) -> Task:
        pass

    @abstractmethod
    def duplicate_task(
        self,
        task_gid: str,
        name: str,
        include: List[str]
    ) -> Task:
        pass

    @abstractmethod
    def get_task_dependencies(self, task_gid: str) -> List[Task]:
        pass

    @abstractmethod
    def set_task_dependencies(self, task_gid: str, dependency_gids: List[str]) -> Task:
        pass

    @abstractmethod
    def remove_task_dependencies(self, task_gid: str, dependency_gids: List[str]) -> Task:
        pass

    @abstractmethod
    def get_task_dependents(self, task_gid: str) -> List[Task]:
        pass

    @abstractmethod
    def set_task_dependents(self, task_gid: str, dependent_gids: List[str]) -> Task:
        pass

    @abstractmethod
    def remove_task_dependents(self, task_gid: str, dependent_gids: List[str]) -> Task:
        pass

