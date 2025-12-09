"""
Interactor for removing a user from a team.
"""
from typing import Dict, Any
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_teams.exceptions.custom_exceptions import (
    TeamDoesNotExistException,
    UserDoesNotExistException
)


class RemoveUserFromTeamInteractor:
    def __init__(
        self,
        storage: StorageInterface
    ):
        self.storage = storage

    def remove_user_from_team(
        self,
        team_gid: str,
        user: str  # Can be "me", email, or GID
    ) -> None:
        """
        Remove a user from a team.
        
        Args:
            team_gid: Team GID (required)
            user: User identifier - can be "me", email, or GID (required)
        """
        # Resolve user identifier to user GID
        user_gid = self._resolve_user_identifier(user)
        
        if not user_gid:
            raise UserDoesNotExistException(f"User not found: {user}")
        
        # Check if team exists
        team = self.storage.get_team(team_gid)
        if not team:
            raise TeamDoesNotExistException()
        
        # Remove user from team
        success = self.storage.remove_user_from_team(
            team_gid=team_gid,
            user_gid=user_gid
        )
        
        if not success:
            raise UserDoesNotExistException(
                f"User {user_gid} is not a member of team {team_gid}"
            )
    
    def _resolve_user_identifier(self, user_identifier: str) -> str:
        """
        Resolve user identifier to user GID.
        Supports "me", email, or GID.
        """
        from asana_users.models.user import User
        
        if user_identifier.lower() == 'me':
            # In a real implementation, this would get the current user
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

