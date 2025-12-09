"""
Create user interactor.
"""
from typing import Dict, Any, Optional
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class CreateUserInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_user_wrapper(
        self,
        name: str,
        email: str,
        photo: Optional[str] = None
    ) -> Dict[str, Any]:
        user = self.storage.create_user(
            name=name,
            email=email,
            photo=photo
        )

        user_dict = {
            'gid': str(user.gid),
            'resource_type': 'user',
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'created_at': user.created_at.isoformat(),
            'modified_at': user.updated_at.isoformat()  # Spec uses modified_at
        }

        return self.presenter.get_user_response(user_dict)


