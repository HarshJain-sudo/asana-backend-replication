"""
Update workspace interactor.
"""
from typing import Dict, Any, Optional
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)


class UpdateWorkspaceInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_workspace_wrapper(
        self,
        workspace_gid: str,
        name: Optional[str] = None,
        is_organization: Optional[bool] = None
    ) -> Dict[str, Any]:
        workspace = self.storage.update_workspace(
            workspace_gid=workspace_gid,
            name=name,
            is_organization=is_organization
        )

        workspace_dict = {
            'gid': str(workspace.gid),
            'name': workspace.name,
            'is_organization': workspace.is_organization,
            'created_at': workspace.created_at.isoformat(),
            'updated_at': workspace.updated_at.isoformat()
        }

        return self.presenter.get_workspace_response(workspace_dict)

