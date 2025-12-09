from typing import Dict, Any
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class RemoveProjectFromTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def remove_project_from_task(
        self,
        task_gid: str,
        project_gid: str
    ) -> Dict[str, Any]:
        task = self.storage.remove_project_from_task(task_gid, project_gid)

        task_dict = {
            'gid': str(task.gid),
            'name': task.name,
        }

        return self.presenter.get_task_response(task_dict)

