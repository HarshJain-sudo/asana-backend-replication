"""
Interactor for adding a user to a team.
"""
from typing import Dict, Any
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_teams.exceptions.custom_exceptions import (
    TeamDoesNotExistException,
    UserDoesNotExistException
)


class AddUserToTeamInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def add_user_to_team(
        self,
        team_gid: str,
        user: str  # Can be "me", email, or GID
    ) -> Dict[str, Any]:
        """
        Add a user to a team.
        
        Args:
            team_gid: Team GID (required)
            user: User identifier - can be "me", email, or GID (required)
        
        Returns:
            Dict containing team membership response data
        """
        # Resolve user identifier to user GID
        user_gid = self._resolve_user_identifier(user)
        
        if not user_gid:
            raise UserDoesNotExistException(f"User not found: {user}")
        
        # Check if team exists
        team = self.storage.get_team(team_gid)
        if not team:
            raise TeamDoesNotExistException()
        
        # Add user to team (creates TeamMembership)
        membership = self.storage.add_user_to_team(
            team_gid=team_gid,
            user_gid=user_gid
        )
        
        # Format response matching TeamMembershipResponse schema
        membership_dict = {
            'gid': str(membership.gid),
            'resource_type': 'team_membership',
            'team': {
                'gid': str(membership.team.gid),
                'resource_type': 'team',
                'name': membership.team.name
            },
            'user': {
                'gid': str(membership.user.gid),
                'resource_type': 'user',
                'name': membership.user.name
            },
            'is_admin': membership.role == 'ADMIN',
            'is_guest': False,  # Not implemented in model yet
            'is_limited_access': False,  # Not implemented in model yet
        }
        
        return self.presenter.get_team_membership_response(membership_dict)
    
    def _resolve_user_identifier(self, user_identifier: str) -> str:
        """
        Resolve user identifier to user GID.
        Supports "me", email, or GID.
        """
        from asana_users.models.user import User
        
        if user_identifier.lower() == 'me':
            # In a real implementation, this would get the current user
            # For now, return None (would need authentication context)
            return None
        
        # Try as email
        try:
            user = User.objects.get(email=user_identifier)
            return str(user.gid)
        except User.DoesNotExist:
            pass
        
        # Try as GID
        try:
            user = User.objects.get(gid=user_identifier)
            return str(user.gid)
        except (User.DoesNotExist, ValueError):
            pass
        
        return None

