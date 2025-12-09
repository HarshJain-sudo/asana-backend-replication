from typing import Dict, Any, List
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetTeamsPresenterImplementation(PresenterInterface):
    def get_team_response(
        self,
        team_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': team_dict
        }

    def get_teams_response(
        self,
        teams_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': teams_list
        }

