import os

# Create interactors
os.makedirs("asana_users/interactors", exist_ok=True)

# Create User Interactor
with open("asana_users/interactors/create_user_interactor.py", "w") as f:
    f.write("""\"\"\"
Create user interactor.
\"\"\"
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
            'name': user.name,
            'email': user.email,
            'photo': user.photo,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }

        return self.presenter.get_user_response(user_dict)
""")

# Update User Interactor
with open("asana_users/interactors/update_user_interactor.py", "w") as f:
    f.write("""\"\"\"
Update user interactor.
\"\"\"
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
""")

# Delete User Interactor
with open("asana_users/interactors/delete_user_interactor.py", "w") as f:
    f.write("""\"\"\"
Delete user interactor.
\"\"\"
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)


class DeleteUserInteractor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def delete_user_wrapper(self, user_gid: str) -> bool:
        result = self.storage.delete_user(user_gid)
        if not result:
            raise UserDoesNotExistException()
        return result
""")

print("✅ Interactors created")
