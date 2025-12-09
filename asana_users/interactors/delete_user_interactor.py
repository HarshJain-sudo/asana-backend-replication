"""
Delete user interactor.
"""
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


