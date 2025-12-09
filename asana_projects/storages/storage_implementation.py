from typing import List, Optional
from asana_projects.models.project import Project
from asana_workspaces.models.workspace import Workspace
from asana_teams.models.team import Team
from asana_tasks.models.task_project import TaskProject
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_project(self, project_gid: str) -> Optional[Project]:
        try:
            return Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return None

    def get_projects(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        archived: Optional[bool] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Project]:
        queryset = Project.objects.all()

        if workspace:
            queryset = queryset.filter(workspace__gid=workspace)
        if team:
            queryset = queryset.filter(team__gid=team)
        if archived is not None:
            queryset = queryset.filter(archived=archived)

        return list(queryset[offset:offset + limit])

    def get_workspace_projects(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Project]:
        return list(
            Project.objects.filter(
                workspace__gid=workspace_gid
            )[offset:offset + limit]
        )

    def create_project(self, name: str, workspace_gid: str, **kwargs) -> Project:
        workspace = Workspace.objects.get(gid=workspace_gid)
        
        project_data = {
            'name': name,
            'workspace': workspace,
        }
        
        # Handle team_gid
        if 'team_gid' in kwargs and kwargs['team_gid']:
            team = Team.objects.get(gid=kwargs.pop('team_gid'))
            project_data['team'] = team
        
        # Add other fields
        project_data.update(kwargs)
        
        project = Project.objects.create(**project_data)
        return project

    def update_project(self, project_gid: str, **update_data) -> Optional[Project]:
        try:
            project = Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return None
        
        for field, value in update_data.items():
            if hasattr(project, field):
                setattr(project, field, value)
        
        project.save()
        return project

    def delete_project(self, project_gid: str) -> bool:
        try:
            project = Project.objects.get(gid=project_gid)
            project.delete()
            return True
        except Project.DoesNotExist:
            return False

    def get_project_tasks(self, project_gid: str, offset: int, limit: int) -> List:
        try:
            project = Project.objects.get(gid=project_gid)
            task_projects = TaskProject.objects.filter(project=project).select_related('task')[offset:offset + limit]
            return [tp.task for tp in task_projects]
        except Project.DoesNotExist:
            return []

