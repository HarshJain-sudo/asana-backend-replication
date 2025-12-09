from typing import Dict, Any, Optional
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.exceptions.custom_exceptions import (
    TaskDoesNotExistException
)


class UpdateTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_task(
        self,
        task_gid: str,
        **update_data
    ) -> Dict[str, Any]:
        task = self.storage.update_task(task_gid, **update_data)

        if not task:
            raise TaskDoesNotExistException()

        task_dict = {
            'gid': str(task.gid),
            'name': task.name,
            'workspace': {
                'gid': str(task.workspace.gid),
                'name': task.workspace.name
            },
            'assignee': {
                'gid': str(task.assignee.gid),
                'name': task.assignee.name
            } if task.assignee else None,
            'assignee_status': task.assignee_status,
            'completed': task.completed,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'due_on': task.due_on.isoformat() if task.due_on else None,
            'due_at': task.due_at.isoformat() if task.due_at else None,
            'notes': task.notes,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
        }

        return self.presenter.get_task_response(task_dict)

