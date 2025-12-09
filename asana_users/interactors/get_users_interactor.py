"""
Interactor for retrieving multiple users.
"""
from typing import Dict, Any, List, Optional
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


class GetUsersInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_users(
        self,
        workspace: Optional[str] = None,
        team: Optional[str] = None,
        opt_fields: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        users = self.storage.get_users(
            workspace=workspace,
            team=team,
            offset=offset,
            limit=limit
        )
        
        # Handle opt_fields (field selection) - for now we return all fields

        # Format users matching UserCompact schema (for list view)
        users_list = [
            {
                'gid': str(user.gid),
                'resource_type': 'user',
                'name': user.name,
            }
            for user in users
        ]

        return self.presenter.get_users_response(users_list)

