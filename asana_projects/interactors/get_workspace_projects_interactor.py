from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_projects.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetWorkspaceProjectsInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_workspace_projects(
        self,
        workspace_gid: str,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        projects = self.storage.get_workspace_projects(
            workspace_gid=workspace_gid,
            offset=offset,
            limit=limit
        )

        projects_list = [
            {
                'gid': str(project.gid),
                'name': project.name,
                'workspace': {
                    'gid': str(project.workspace.gid),
                    'name': project.workspace.name
                },
                'team': {
                    'gid': str(project.team.gid),
                    'name': project.team.name
                } if project.team else None,
                'public': project.public,
                'archived': project.archived,
                'color': project.color,
                'due_date': project.due_date.isoformat() if project.due_date else None,
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat(),
            }
            for project in projects
        ]

        return self.presenter.get_projects_response(projects_list)

