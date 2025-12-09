from typing import Dict, Any
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_teams.exceptions.custom_exceptions import (
    TeamDoesNotExistException
)


class GetTeamInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_team(self, team_gid: str) -> Dict[str, Any]:
        team = self.storage.get_team(team_gid)

        if not team:
            raise TeamDoesNotExistException()

        team_dict = {
            'gid': str(team.gid),
            'name': team.name,
            'workspace': {
                'gid': str(team.workspace.gid),
                'name': team.workspace.name
            },
            'description': team.description,
            'created_at': team.created_at.isoformat(),
            'updated_at': team.updated_at.isoformat(),
        }

        return self.presenter.get_team_response(team_dict)

