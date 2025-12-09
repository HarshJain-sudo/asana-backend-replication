from typing import Dict, Any, Optional
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_teams.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetTeamsInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_teams(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        teams = self.storage.get_teams(
            workspace_gid=workspace_gid,
            offset=offset,
            limit=limit
        )

        teams_list = [
            {
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
            for team in teams
        ]

        return self.presenter.get_teams_response(teams_list)

