from typing import Dict, Any
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class CreateTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_task(
        self,
        name: str,
        workspace: str = None,  # New API spec format
        workspace_gid: str = None,  # Legacy format
        assignee: str = None,  # New API spec format
        assignee_gid: str = None,  # Legacy format
        projects: list = None,
        tags: list = None,
        followers: list = None,
        **kwargs
    ) -> Dict[str, Any]:
        # Support both new (workspace) and legacy (workspace_gid) formats
        workspace_id = workspace or workspace_gid
        assignee_id = assignee or assignee_gid
        
        task = self.storage.create_task(
            name=name,
            workspace_gid=workspace_id,
            assignee_gid=assignee_id,
            **kwargs
        )
        
        # Handle create-only fields (projects, tags, followers)
        if projects:
            for project_gid in projects:
                try:
                    self.storage.add_project_to_task(str(task.gid), project_gid)
                except Exception:
                    pass  # Ignore errors for now
        
        if tags:
            for tag_gid in tags:
                try:
                    self.storage.add_tag_to_task(str(task.gid), tag_gid)
                except Exception:
                    pass
        
        if followers:
            self.storage.add_followers_to_task(str(task.gid), followers)

        # Format response matching TaskResponse schema
        task_dict = {
            'gid': str(task.gid),
            'resource_type': 'task',
            'name': task.name,
            'resource_subtype': 'default_task',  # Default value
            'workspace': {
                'gid': str(task.workspace.gid),
                'resource_type': 'workspace',
                'name': task.workspace.name
            },
            'assignee': {
                'gid': str(task.assignee.gid),
                'resource_type': 'user',
                'name': task.assignee.name
            } if task.assignee else None,
            'assignee_status': task.assignee_status,
            'completed': task.completed,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'due_on': task.due_on.isoformat() if task.due_on else None,
            'due_at': task.due_at.isoformat() if task.due_at else None,
            'start_on': task.start_on.isoformat() if task.start_on else None,
            'start_at': task.start_at.isoformat() if task.start_at else None,
            'notes': task.notes,
            'html_notes': task.html_notes,
            'num_hearts': task.num_hearts,
            'num_likes': task.num_likes,
            'created_at': task.created_at.isoformat(),
            'modified_at': task.updated_at.isoformat(),  # Spec uses modified_at
        }

        return self.presenter.get_task_response(task_dict)

