from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_projects.exceptions.custom_exceptions import (
    ProjectDoesNotExistException
)


class GetProjectInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_project(self, project_gid: str) -> Dict[str, Any]:
        project = self.storage.get_project(project_gid)

        if not project:
            raise ProjectDoesNotExistException()

        project_dict = {
            'gid': str(project.gid),
            'resource_type': 'project',
            'name': project.name,
            'workspace': {
                'gid': str(project.workspace.gid),
                'resource_type': 'workspace',
                'name': project.workspace.name
            },
            'team': {
                'gid': str(project.team.gid),
                'resource_type': 'team',
                'name': project.team.name
            } if project.team else None,
            'public': project.public,
            'archived': project.archived,
            'color': project.color,
            'notes': project.notes,
            'due_on': project.due_date.isoformat() if project.due_date else None,  # Spec uses due_on
            'start_on': project.start_on.isoformat() if project.start_on else None,
            'created_at': project.created_at.isoformat(),
            'modified_at': project.updated_at.isoformat(),  # Spec uses modified_at
            'created_by': {
                'gid': str(project.created_by.gid),
                'resource_type': 'user',
                'name': project.created_by.name
            } if project.created_by else None,
        }

        return self.presenter.get_project_response(project_dict)

