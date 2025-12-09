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


class GetTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_task(self, task_gid: str) -> Dict[str, Any]:
        task = self.storage.get_task(task_gid)

        if not task:
            raise TaskDoesNotExistException()

        # Get related objects
        from asana_tasks.models.task_project import TaskProject
        from asana_tasks.models.task_tag import TaskTag
        from asana_tasks.models.task_follower import TaskFollower
        
        task_projects = TaskProject.objects.filter(task=task).select_related('project')
        task_tags = TaskTag.objects.filter(task=task).select_related('tag')
        task_followers = TaskFollower.objects.filter(task=task).select_related('user')
        
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
            'modified_at': task.updated_at.isoformat(),
            'created_by': {
                'gid': str(task.created_by.gid),
                'resource_type': 'user',
                'name': task.created_by.name
            } if task.created_by else None,
            # Nested arrays matching API spec
            'projects': [
                {
                    'gid': str(tp.project.gid),
                    'resource_type': 'project',
                    'name': tp.project.name
                }
                for tp in task_projects
            ],
            'tags': [
                {
                    'gid': str(tt.tag.gid),
                    'resource_type': 'tag',
                    'name': tt.tag.name
                }
                for tt in task_tags
            ],
            'followers': [
                {
                    'gid': str(tf.user.gid),
                    'resource_type': 'user',
                    'name': tf.user.name
                }
                for tf in task_followers
            ],
        }

        return self.presenter.get_task_response(task_dict)

