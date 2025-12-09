from abc import ABC, abstractmethod
from typing import List, Optional
from asana_teams.models.team import Team


class StorageInterface(ABC):
    @abstractmethod
    def get_team(self, team_gid: str) -> Optional[Team]:
        pass

    @abstractmethod
    def get_teams(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        pass

    @abstractmethod
    def get_workspace_teams(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        pass
    
    @abstractmethod
    def create_team(
        self,
        name: str,
        workspace_gid: str,
        description: str = None,
        **kwargs
    ) -> Team:
        pass
    
    @abstractmethod
    def update_team(
        self,
        team_gid: str,
        name: str = None,
        description: str = None,
        **kwargs
    ) -> Team:
        pass
    
    @abstractmethod
    def add_user_to_team(
        self,
        team_gid: str,
        user_gid: str
    ):
        pass
    
    @abstractmethod
    def remove_user_from_team(
        self,
        team_gid: str,
        user_gid: str
    ) -> bool:
        pass
    
    @abstractmethod
    def get_teams_for_user(
        self,
        user_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        pass

