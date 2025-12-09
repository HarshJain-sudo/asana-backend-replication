"""
Interactor for creating a team.
"""
from typing import Dict, Any
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_teams.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)


class CreateTeamInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_team(
        self,
        name: str,
        workspace: str,
        description: str = None,
        html_description: str = None,
        visibility: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new team.
        
        Args:
            name: Team name (required)
            workspace: Workspace GID (required)
            description: Team description (optional)
            html_description: HTML formatted description (optional)
            visibility: Team visibility - secret, request_to_join, or public (optional)
        
        Returns:
            Dict containing team response data
        """
        # Validate visibility if provided
        if visibility and visibility not in ['secret', 'request_to_join', 'public']:
            raise ValueError(
                f"visibility must be one of: secret, request_to_join, public. Got: {visibility}"
            )
        
        team = self.storage.create_team(
            name=name,
            workspace_gid=workspace,
            description=description or html_description,  # Use description or html_description
            **kwargs
        )
        
        # Format response matching TeamResponse schema
        team_dict = {
            'gid': str(team.gid),
            'resource_type': 'team',
            'name': team.name,
            'description': team.description,
            'workspace': {
                'gid': str(team.workspace.gid),
                'resource_type': 'workspace',
                'name': team.workspace.name
            },
            'created_at': team.created_at.isoformat(),
            'modified_at': team.updated_at.isoformat(),
        }
        
        return self.presenter.get_team_response(team_dict)

