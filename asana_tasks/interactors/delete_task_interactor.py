from typing import Dict, Any
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.exceptions.custom_exceptions import (
    TaskDoesNotExistException
)


class DeleteTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def delete_task(self, task_gid: str) -> Dict[str, Any]:
        success = self.storage.delete_task(task_gid)

        if not success:
            raise TaskDoesNotExistException()

        return self.presenter.get_delete_response()

