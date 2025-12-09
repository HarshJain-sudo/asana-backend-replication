from typing import Dict, Any, Optional
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tasks.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetTasksInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_tasks(
        self,
        workspace: Optional[str] = None,
        assignee: Optional[str] = None,
        project: Optional[str] = None,
        section: Optional[str] = None,
        completed_since: Optional[str] = None,
        modified_since: Optional[str] = None,
        opt_fields: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        tasks = self.storage.get_tasks(
            workspace=workspace,
            assignee=assignee,
            project=project,
            section=section,
            completed_since=completed_since,
            modified_since=modified_since,
            offset=offset,
            limit=limit
        )
        
        # Handle opt_fields (field selection) - for now we return all fields
        # In a full implementation, we would filter the response based on opt_fields

        # Format tasks matching TaskCompact schema
        tasks_list = []
        for task in tasks:
            task_dict = {
                'gid': str(task.gid),
                'resource_type': 'task',
                'name': task.name,
                'resource_subtype': 'default_task',
            }
            tasks_list.append(task_dict)

        return self.presenter.get_tasks_response(tasks_list)

