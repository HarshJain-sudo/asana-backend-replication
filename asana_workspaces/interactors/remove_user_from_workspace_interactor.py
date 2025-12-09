"""
Interactor for removing a user from a workspace.
"""
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class RemoveUserFromWorkspaceInteractor:
    def __init__(
        self,
        storage: StorageInterface
    ):
        self.storage = storage

    def remove_user_from_workspace(
        self,
        workspace_gid: str,
        user: str  # Can be "me", email, or GID
    ) -> None:
        """
        Remove a user from a workspace.
        
        Args:
            workspace_gid: Workspace GID (required)
            user: User identifier - can be "me", email, or GID (required)
        """
        # Resolve user identifier to user GID
        user_gid = self._resolve_user_identifier(user)
        
        if not user_gid:
            raise UserDoesNotExistException(f"User not found: {user}")
        
        # Check if workspace exists
        workspace = self.storage.get_workspace(workspace_gid)
        if not workspace:
            raise WorkspaceDoesNotExistException()
        
        # Remove user from workspace
        success = self.storage.remove_user_from_workspace(
            workspace_gid=workspace_gid,
            user_gid=user_gid
        )
        
        if not success:
            raise UserDoesNotExistException(
                f"User {user_gid} is not a member of workspace {workspace_gid}"
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

