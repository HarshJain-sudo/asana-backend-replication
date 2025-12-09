"""
Update user interactor.
"""
from typing import Dict, Any, Optional
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class UpdateUserInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_user_wrapper(
        self,
        user_gid: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        photo: Optional[str] = None
    ) -> Dict[str, Any]:
        user = self.storage.update_user(
            user_gid=user_gid,
            name=name,
            email=email,
            photo=photo
        )

        user_dict = {
            'gid': str(user.gid),
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }

        return self.presenter.get_user_response(user_dict)


