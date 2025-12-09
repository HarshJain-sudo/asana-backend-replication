from typing import Dict, Any, Optional
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


class GetProjectsInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_projects(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        archived: Optional[bool] = None,
        opt_fields: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        projects = self.storage.get_projects(
            workspace=workspace,
            team=team,
            archived=archived,
            offset=offset,
            limit=limit
        )
        
        # Handle opt_fields (field selection) - for now we return all fields
        # In a full implementation, we would filter the response based on opt_fields

        # Format projects matching ProjectCompact schema (for list view)
        projects_list = [
            {
                'gid': str(project.gid),
                'resource_type': 'project',
                'name': project.name,
            }
            for project in projects
        ]

        return self.presenter.get_projects_response(projects_list)

