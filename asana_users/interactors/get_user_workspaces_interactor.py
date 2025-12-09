"""
Interactor for retrieving user workspaces.
"""
from typing import Dict, Any, List
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_users.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class GetUserWorkspacesInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_user_workspaces(
        self,
        user_gid: str,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        workspaces = self.storage.get_user_workspaces(
            user_gid=user_gid,
            offset=offset,
            limit=limit
        )

        workspaces_list = [
            {
                'gid': str(workspace.gid),
                'name': workspace.name,
                'is_organization': workspace.is_organization,
                'created_at': workspace.created_at.isoformat(),
                'updated_at': workspace.updated_at.isoformat(),
            }
            for workspace in workspaces
        ]

        return self.presenter.get_user_workspaces_response(
            workspaces_list
        )

