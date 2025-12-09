"""
Interactor for retrieving a single user.
"""
from typing import Dict, Any
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class GetUserInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_user(self, user_gid: str) -> Dict[str, Any]:
        user = self.storage.get_user(user_gid)

        if not user:
            raise UserDoesNotExistException()

        user_dict = {
            'gid': str(user.gid),
            'resource_type': 'user',
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'created_at': user.created_at.isoformat(),
            'modified_at': user.updated_at.isoformat(),  # Spec uses modified_at
        }

        return self.presenter.get_user_response(user_dict)

