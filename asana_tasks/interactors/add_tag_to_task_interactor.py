from typing import Dict, Any
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class AddTagToTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def add_tag_to_task(
        self,
        task_gid: str,
        tag_gid: str
    ) -> Dict[str, Any]:
        task = self.storage.add_tag_to_task(task_gid, tag_gid)

        task_dict = {
            'gid': str(task.gid),
            'name': task.name,
        }

        return self.presenter.get_task_response(task_dict)

