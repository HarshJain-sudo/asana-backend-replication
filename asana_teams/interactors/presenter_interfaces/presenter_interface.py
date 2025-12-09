from abc import ABC, abstractmethod
from typing import Dict, Any, List


class PresenterInterface(ABC):
    @abstractmethod
    def get_team_response(
        self,
        team_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_teams_response(
        self,
        teams_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_team_membership_response(
        self,
        membership_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        pass

