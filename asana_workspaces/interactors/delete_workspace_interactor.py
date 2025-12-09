"""
Delete workspace interactor.
"""
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)


class DeleteWorkspaceInteractor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def delete_workspace_wrapper(self, workspace_gid: str) -> bool:
        result = self.storage.delete_workspace(workspace_gid)
        if not result:
            raise WorkspaceDoesNotExistException()
        return result

