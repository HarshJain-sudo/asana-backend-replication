"""
Interactor for updating a team.
"""
from typing import Dict, Any, Optional
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_teams.exceptions.custom_exceptions import (
    TeamDoesNotExistException
)


class UpdateTeamInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_team(
        self,
        team_gid: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        html_description: Optional[str] = None,
        visibility: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing team.
        
        Args:
            team_gid: Team GID (required)
            name: Team name (optional)
            description: Team description (optional)
            html_description: HTML formatted description (optional)
            visibility: Team visibility (optional)
        
        Returns:
            Dict containing updated team response data
        """
        # Validate visibility if provided
        if visibility and visibility not in ['secret', 'request_to_join', 'public']:
            raise ValueError(
                f"visibility must be one of: secret, request_to_join, public. Got: {visibility}"
            )
        
        # Use description or html_description (prefer description)
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if description is not None:
            update_data['description'] = description
        elif html_description is not None:
            update_data['description'] = html_description
        
        team = self.storage.update_team(
            team_gid=team_gid,
            **update_data
        )
        
        if not team:
            raise TeamDoesNotExistException()
        
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

