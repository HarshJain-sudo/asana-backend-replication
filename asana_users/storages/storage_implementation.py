"""
Storage implementation for user operations.
"""
from typing import List, Optional
from asana_users.models.user import User
from asana_users.models.user_workspace_membership import (
    UserWorkspaceMembership
)
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class StorageImplementation(StorageInterface):
    def create_user(
        self,
        name: str,
        email: str,
        photo: Optional[str] = None
    ) -> User:
        user = User.objects.create(
            name=name,
            email=email,
            photo=photo
        )
        return user

    def get_user(self, user_gid: str) -> Optional[User]:
        try:
            return User.objects.get(gid=user_gid)
        except User.DoesNotExist:
            return None

    def get_users(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[User]:
        from asana_teams.models.team_membership import TeamMembership
        
        queryset = User.objects.all()
        
        if workspace:
            try:
                # Filter users by workspace membership
                workspace_user_ids = UserWorkspaceMembership.objects.filter(
                    workspace__gid=workspace
                ).values_list('user_id', flat=True)
                queryset = queryset.filter(id__in=workspace_user_ids)
            except Exception:
                # If workspace filtering fails, just return all users
                pass
        
        if team:
            try:
                # Filter users by team membership
                team_user_ids = TeamMembership.objects.filter(
                    team__gid=team
                ).values_list('user_id', flat=True)
                queryset = queryset.filter(id__in=team_user_ids)
            except Exception:
                # If team filtering fails, just return all users
                pass
        
        return list(queryset[offset:offset + limit])

    def update_user(
        self,
        user_gid: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        photo: Optional[str] = None
    ) -> User:
        user = self.get_user(user_gid)
        if not user:
            raise UserDoesNotExistException()

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if photo is not None:
            user.photo = photo

        user.save()
        return user

    def delete_user(self, user_gid: str) -> bool:
        user = self.get_user(user_gid)
        if not user:
            return False

        user.delete()
        return True

    def get_user_workspaces(
        self,
        user_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List:
        user = self.get_user(user_gid)
        if not user:
            raise UserDoesNotExistException()

        memberships = UserWorkspaceMembership.objects.filter(
            user=user
        )[offset:offset + limit]

        return [
            membership.workspace
            for membership in memberships
        ]

