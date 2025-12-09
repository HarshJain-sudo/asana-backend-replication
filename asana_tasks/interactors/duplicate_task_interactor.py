from typing import Dict, Any, List, Optional
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException


class DuplicateTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def duplicate_task(
        self,
        task_gid: str,
        name: Optional[str] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        original_task = self.storage.get_task(task_gid)
        if not original_task:
            raise TaskDoesNotExistException(f"Task with GID '{task_gid}' does not exist.")

        # Default name if not provided
        if not name:
            name = f"{original_task.name} (Copy)"

        # Create duplicated task
        new_task = self.storage.duplicate_task(
            task_gid=task_gid,
            name=name,
            include=include or []
        )

        # Format response
        task_dict = {
            'gid': str(new_task.gid),
            'resource_type': 'task',
            'name': new_task.name,
            'workspace': {
                'gid': str(new_task.workspace.gid),
                'resource_type': 'workspace',
                'name': new_task.workspace.name
            },
            'assignee': {
                'gid': str(new_task.assignee.gid),
                'resource_type': 'user',
                'name': new_task.assignee.name
            } if new_task.assignee and 'assignee' in (include or []) else None,
            'completed': new_task.completed,
            'completed_at': new_task.completed_at.isoformat() if new_task.completed_at else None,
            'due_on': str(new_task.due_on) if new_task.due_on else None,
            'due_at': new_task.due_at.isoformat() if new_task.due_at else None,
            'start_on': str(new_task.start_on) if new_task.start_on else None,
            'start_at': new_task.start_at.isoformat() if new_task.start_at else None,
            'notes': new_task.notes if 'notes' in (include or []) else None,
            'html_notes': new_task.html_notes if 'notes' in (include or []) else None,
            'created_at': new_task.created_at.isoformat(),
            'updated_at': new_task.updated_at.isoformat(),
        }

        return self.presenter.get_task_response(task_dict)

