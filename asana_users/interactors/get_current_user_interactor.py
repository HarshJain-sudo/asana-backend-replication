"""
Interactor for retrieving current authenticated user.
"""
from typing import Dict, Any
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_users.exceptions.custom_exceptions import (
    UserNotAuthenticatedException
)


class GetCurrentUserInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_current_user(self, user_gid: str) -> Dict[str, Any]:
        if not user_gid:
            raise UserNotAuthenticatedException()

        user = self.storage.get_user(user_gid)

        if not user:
            raise UserNotAuthenticatedException()

        user_dict = {
            'gid': str(user.gid),
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
        }

        return self.presenter.get_user_response(user_dict)

