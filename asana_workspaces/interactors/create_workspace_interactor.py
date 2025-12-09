"""
Create workspace interactor.
"""
from typing import Dict, Any
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class CreateWorkspaceInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_workspace_wrapper(
        self,
        name: str,
        is_organization: bool = False
    ) -> Dict[str, Any]:
        workspace = self.storage.create_workspace(
            name=name,
            is_organization=is_organization
        )

        workspace_dict = {
            'gid': str(workspace.gid),
            'resource_type': 'workspace',
            'name': workspace.name,
            'is_organization': workspace.is_organization,
            'created_at': workspace.created_at.isoformat(),
            'modified_at': workspace.updated_at.isoformat()  # Spec uses modified_at
        }

        return self.presenter.get_workspace_response(workspace_dict)

