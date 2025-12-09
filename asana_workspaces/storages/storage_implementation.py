"""
Storage implementation for workspace operations.
"""
from typing import List, Optional
from asana_workspaces.models.workspace import Workspace
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)


class StorageImplementation(StorageInterface):
    def create_workspace(
        self,
        name: str,
        is_organization: bool = False
    ) -> Workspace:
        workspace = Workspace.objects.create(
            name=name,
            is_organization=is_organization
        )
        return workspace

    def get_workspace(self, workspace_gid: str) -> Optional[Workspace]:
        try:
            return Workspace.objects.get(gid=workspace_gid)
        except Workspace.DoesNotExist:
            return None

    def get_workspaces(
        self,
        offset: int = 0,
        limit: int = 50
    ) -> List[Workspace]:
        return list(
            Workspace.objects.all()[offset:offset + limit]
        )
    
    def get_workspaces_count(self) -> int:
        """Get total count of workspaces for pagination."""
        return Workspace.objects.count()

    def update_workspace(
        self,
        workspace_gid: str,
        name: Optional[str] = None,
        is_organization: Optional[bool] = None
    ) -> Workspace:
        workspace = self.get_workspace(workspace_gid)
        if not workspace:
            raise WorkspaceDoesNotExistException()

        if name is not None:
            workspace.name = name
        if is_organization is not None:
            workspace.is_organization = is_organization

        workspace.save()
        return workspace

    def delete_workspace(self, workspace_gid: str) -> bool:
        workspace = self.get_workspace(workspace_gid)
        if not workspace:
            return False

        workspace.delete()
        return True
    
    def add_user_to_workspace(
        self,
        workspace_gid: str,
        user_gid: str
    ):
        from asana_users.models.user_workspace_membership import (
            UserWorkspaceMembership
        )
        from asana_users.models.user import User
        
        workspace = self.get_workspace(workspace_gid)
        if not workspace:
            return None
        
        try:
            user = User.objects.get(gid=user_gid)
        except User.DoesNotExist:
            return None
        
        # Check if membership already exists
        membership, created = UserWorkspaceMembership.objects.get_or_create(
            workspace=workspace,
            user=user
        )
        
        return membership
    
    def remove_user_from_workspace(
        self,
        workspace_gid: str,
        user_gid: str
    ) -> bool:
        from asana_users.models.user_workspace_membership import (
            UserWorkspaceMembership
        )
        from asana_users.models.user import User
        
        try:
            user = User.objects.get(gid=user_gid)
        except User.DoesNotExist:
            return False
        
        try:
            membership = UserWorkspaceMembership.objects.get(
                workspace__gid=workspace_gid,
                user=user
            )
            membership.delete()
            return True
        except UserWorkspaceMembership.DoesNotExist:
            return False
    
    def get_workspace_events(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List:
        """
        Get workspace events.
        For now, returns empty list as Events model is not implemented.
        """
        # Events would require an Event model
        # For now, return empty list
        return []

