from typing import Dict, Any, List
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException


class RemoveTaskDependenciesInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def remove_task_dependencies(
        self,
        task_gid: str,
        dependency_gids: List[str]
    ) -> Dict[str, Any]:
        task = self.storage.get_task(task_gid)
        if not task:
            raise TaskDoesNotExistException(f"Task with GID '{task_gid}' does not exist.")

        updated_task = self.storage.remove_task_dependencies(task_gid, dependency_gids)

        task_dict = {
            'gid': str(updated_task.gid),
            'resource_type': 'task',
            'name': updated_task.name,
            'workspace': {
                'gid': str(updated_task.workspace.gid),
                'resource_type': 'workspace',
                'name': updated_task.workspace.name
            },
            'completed': updated_task.completed,
            'created_at': updated_task.created_at.isoformat(),
            'updated_at': updated_task.updated_at.isoformat(),
        }

        return self.presenter.get_task_response(task_dict)

