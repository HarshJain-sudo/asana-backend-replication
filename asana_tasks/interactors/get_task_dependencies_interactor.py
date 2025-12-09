from typing import Dict, Any, List
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException


class GetTaskDependenciesInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_task_dependencies(self, task_gid: str) -> Dict[str, Any]:
        task = self.storage.get_task(task_gid)
        if not task:
            raise TaskDoesNotExistException(f"Task with GID '{task_gid}' does not exist.")

        dependencies = self.storage.get_task_dependencies(task_gid)

        dependencies_list = [
            {
                'gid': str(dep.gid),
                'resource_type': 'task',
                'name': dep.name,
                'workspace': {
                    'gid': str(dep.workspace.gid),
                    'resource_type': 'workspace',
                    'name': dep.workspace.name
                },
                'completed': dep.completed,
                'created_at': dep.created_at.isoformat(),
                'updated_at': dep.updated_at.isoformat(),
            }
            for dep in dependencies
        ]

        return self.presenter.get_tasks_response(dependencies_list)

