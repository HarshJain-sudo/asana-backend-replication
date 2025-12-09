"""
Interactor for adding a user to a workspace.
"""
from typing import Dict, Any
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class AddUserToWorkspaceInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def add_user_to_workspace(
        self,
        workspace_gid: str,
        user: str  # Can be "me", email, or GID
    ) -> Dict[str, Any]:
        """
        Add a user to a workspace.
        
        Args:
            workspace_gid: Workspace GID (required)
            user: User identifier - can be "me", email, or GID (required)
        
        Returns:
            Dict containing user response data
        """
        # Resolve user identifier to user GID
        user_gid = self._resolve_user_identifier(user)
        
        if not user_gid:
            raise UserDoesNotExistException(f"User not found: {user}")
        
        # Check if workspace exists
        workspace = self.storage.get_workspace(workspace_gid)
        if not workspace:
            raise WorkspaceDoesNotExistException()
        
        # Add user to workspace (creates UserWorkspaceMembership)
        membership = self.storage.add_user_to_workspace(
            workspace_gid=workspace_gid,
            user_gid=user_gid
        )
        
        # Format response matching UserBaseResponse schema
        user_dict = {
            'gid': str(membership.user.gid),
            'resource_type': 'user',
            'name': membership.user.name,
            'email': membership.user.email,
            'photo': membership.user.photo,
        }
        
        return self.presenter.get_user_response(user_dict)
    
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

