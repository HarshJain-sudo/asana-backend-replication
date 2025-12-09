from typing import List, Optional
from asana_teams.models.team import Team
from asana_teams.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_team(self, team_gid: str) -> Optional[Team]:
        try:
            return Team.objects.get(gid=team_gid)
        except Team.DoesNotExist:
            return None

    def get_teams(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        queryset = Team.objects.all()

        if workspace_gid:
            queryset = queryset.filter(workspace__gid=workspace_gid)

        return list(queryset[offset:offset + limit])

    def get_workspace_teams(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        return list(
            Team.objects.filter(
                workspace__gid=workspace_gid
            )[offset:offset + limit]
        )
    
    def create_team(
        self,
        name: str,
        workspace_gid: str,
        description: str = None,
        **kwargs
    ) -> Team:
        from asana_workspaces.models.workspace import Workspace
        from asana_workspaces.exceptions.custom_exceptions import (
            WorkspaceDoesNotExistException
        )
        
        try:
            workspace = Workspace.objects.get(gid=workspace_gid)
        except Workspace.DoesNotExist:
            raise WorkspaceDoesNotExistException()
        
        team = Team.objects.create(
            name=name,
            workspace=workspace,
            description=description,
            **kwargs
        )
        return team
    
    def update_team(
        self,
        team_gid: str,
        name: str = None,
        description: str = None,
        **kwargs
    ) -> Team:
        team = self.get_team(team_gid)
        if not team:
            return None
        
        if name is not None:
            team.name = name
        if description is not None:
            team.description = description
        
        for key, value in kwargs.items():
            if hasattr(team, key):
                setattr(team, key, value)
        
        team.save()
        return team
    
    def add_user_to_team(
        self,
        team_gid: str,
        user_gid: str
    ):
        from asana_teams.models.team_membership import TeamMembership
        from asana_users.models.user import User
        
        team = self.get_team(team_gid)
        if not team:
            return None
        
        try:
            user = User.objects.get(gid=user_gid)
        except User.DoesNotExist:
            return None
        
        # Check if membership already exists
        membership, created = TeamMembership.objects.get_or_create(
            team=team,
            user=user,
            defaults={'role': 'MEMBER'}
        )
        
        return membership
    
    def remove_user_from_team(
        self,
        team_gid: str,
        user_gid: str
    ) -> bool:
        from asana_teams.models.team_membership import TeamMembership
        from asana_users.models.user import User
        
        try:
            user = User.objects.get(gid=user_gid)
        except User.DoesNotExist:
            return False
        
        try:
            membership = TeamMembership.objects.get(
                team__gid=team_gid,
                user=user
            )
            membership.delete()
            return True
        except TeamMembership.DoesNotExist:
            return False
    
    def get_teams_for_user(
        self,
        user_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Team]:
        from asana_teams.models.team_membership import TeamMembership
        
        memberships = TeamMembership.objects.filter(
            user__gid=user_gid
        ).select_related('team')[offset:offset + limit]
        
        return [membership.team for membership in memberships]

