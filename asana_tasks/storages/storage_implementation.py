from typing import List, Optional
from django.db import transaction
from django.db.models import Q
from asana_tasks.models.task import Task
from asana_tasks.models.task_project import TaskProject
from asana_tasks.models.task_tag import TaskTag
from asana_tasks.models.task_follower import TaskFollower
from asana_tasks.models.task_dependency import TaskDependency
from asana_workspaces.models.workspace import Workspace
from asana_users.models.user import User
from asana_projects.models.project import Project
from asana_tags.models.tag import Tag
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.exceptions.custom_exceptions import (
    TaskDoesNotExistException
)


class StorageImplementation(StorageInterface):
    def get_task(self, task_gid: str) -> Optional[Task]:
        try:
            return Task.objects.get(gid=task_gid)
        except Task.DoesNotExist:
            return None

    def get_tasks(
        self,
        workspace: Optional[str] = None,
        assignee: Optional[str] = None,
        project: Optional[str] = None,
        section: Optional[str] = None,
        completed_since: Optional[str] = None,
        modified_since: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Task]:
        from django.utils import timezone
        from datetime import datetime
        
        queryset = Task.objects.all()

        if workspace:
            queryset = queryset.filter(workspace__gid=workspace)
        
        if assignee:
            # Handle assignee.any = null for unassigned tasks
            if assignee.lower() == 'null':
                queryset = queryset.filter(assignee__isnull=True)
            else:
                queryset = queryset.filter(assignee__gid=assignee)
        
        if project:
            queryset = queryset.filter(taskproject__project__gid=project).distinct()
        
        if section:
            # Section filtering would require Section model (not implemented yet)
            # For now, we'll skip this filter
            pass
        
        if completed_since:
            try:
                completed_since_dt = datetime.fromisoformat(completed_since.replace('Z', '+00:00'))
                # Return incomplete tasks OR tasks completed since this time
                queryset = queryset.filter(
                    Q(completed=False) | 
                    Q(completed=True, completed_at__gte=completed_since_dt)
                )
            except (ValueError, AttributeError):
                pass  # Invalid date format, ignore filter
        
        if modified_since:
            try:
                modified_since_dt = datetime.fromisoformat(modified_since.replace('Z', '+00:00'))
                queryset = queryset.filter(updated_at__gte=modified_since_dt)
            except (ValueError, AttributeError):
                pass  # Invalid date format, ignore filter

        return list(queryset[offset:offset + limit])

    def create_task(
        self,
        name: str,
        workspace_gid: str,
        assignee_gid: Optional[str] = None,
        **kwargs
    ) -> Task:
        workspace = Workspace.objects.get(gid=workspace_gid)
        
        task_data = {
            'name': name,
            'workspace': workspace,
            **kwargs
        }
        
        if assignee_gid:
            assignee = User.objects.get(gid=assignee_gid)
            task_data['assignee'] = assignee
        
        task = Task.objects.create(**task_data)
        return task

    def update_task(self, task_gid: str, **update_data) -> Optional[Task]:
        task = self.get_task(task_gid)
        if not task:
            return None
        
        if 'assignee_gid' in update_data:
            assignee_gid = update_data.pop('assignee_gid')
            if assignee_gid:
                task.assignee = User.objects.get(gid=assignee_gid)
            else:
                task.assignee = None
        
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        task.save()
        return task

    def delete_task(self, task_gid: str) -> bool:
        task = self.get_task(task_gid)
        if not task:
            return False
        task.delete()
        return True

    @transaction.atomic
    def add_project_to_task(self, task_gid: str, project_gid: str) -> Task:
        task = Task.objects.get(gid=task_gid)
        project = Project.objects.get(gid=project_gid)
        TaskProject.objects.get_or_create(task=task, project=project)
        return task

    @transaction.atomic
    def remove_project_from_task(self, task_gid: str, project_gid: str) -> Task:
        task = Task.objects.get(gid=task_gid)
        project = Project.objects.get(gid=project_gid)
        TaskProject.objects.filter(task=task, project=project).delete()
        return task

    @transaction.atomic
    def add_tag_to_task(self, task_gid: str, tag_gid: str) -> Task:
        task = Task.objects.get(gid=task_gid)
        tag = Tag.objects.get(gid=tag_gid)
        TaskTag.objects.get_or_create(task=task, tag=tag)
        return task

    @transaction.atomic
    def remove_tag_from_task(self, task_gid: str, tag_gid: str) -> Task:
        task = Task.objects.get(gid=task_gid)
        tag = Tag.objects.get(gid=tag_gid)
        TaskTag.objects.filter(task=task, tag=tag).delete()
        return task

    @transaction.atomic
    def add_followers_to_task(self, task_gid: str, follower_gids: List[str]) -> Task:
        task = Task.objects.get(gid=task_gid)
        for follower_gid in follower_gids:
            user = User.objects.get(gid=follower_gid)
            TaskFollower.objects.get_or_create(task=task, user=user)
        return task

    @transaction.atomic
    def remove_followers_from_task(self, task_gid: str, follower_gids: List[str]) -> Task:
        task = Task.objects.get(gid=task_gid)
        TaskFollower.objects.filter(
            task=task,
            user__gid__in=follower_gids
        ).delete()
        return task

    @transaction.atomic
    def duplicate_task(
        self,
        task_gid: str,
        name: str,
        include: List[str]
    ) -> Task:
        original_task = Task.objects.get(gid=task_gid)
        
        # Create new task with copied fields
        new_task = Task.objects.create(
            name=name,
            workspace=original_task.workspace,
            assignee=original_task.assignee if 'assignee' in include else None,
            assignee_status=original_task.assignee_status,
            completed=False,  # New task is not completed
            due_on=original_task.due_on if 'due_on' in include else None,
            due_at=original_task.due_at if 'due_at' in include else None,
            start_on=original_task.start_on if 'start_on' in include else None,
            start_at=original_task.start_at if 'start_at' in include else None,
            notes=original_task.notes if 'notes' in include else None,
            html_notes=original_task.html_notes if 'notes' in include else None,
            created_by=original_task.created_by
        )
        
        # Copy relationships if included
        if 'projects' in include:
            for task_project in TaskProject.objects.filter(task=original_task):
                TaskProject.objects.create(task=new_task, project=task_project.project)
        
        if 'tags' in include:
            for task_tag in TaskTag.objects.filter(task=original_task):
                TaskTag.objects.create(task=new_task, tag=task_tag.tag)
        
        if 'followers' in include:
            for task_follower in TaskFollower.objects.filter(task=original_task):
                TaskFollower.objects.create(task=new_task, user=task_follower.user)
        
        # Note: subtasks and dependencies are typically not duplicated by default
        # but can be added if needed
        
        return new_task

    def get_task_dependencies(self, task_gid: str) -> List[Task]:
        """Get tasks that this task depends on (predecessors)."""
        task = Task.objects.get(gid=task_gid)
        dependencies = TaskDependency.objects.filter(successor=task).select_related('predecessor')
        return [dep.predecessor for dep in dependencies]

    @transaction.atomic
    def set_task_dependencies(self, task_gid: str, dependency_gids: List[str]) -> Task:
        """Set dependencies for a task (tasks that must complete before this task)."""
        task = Task.objects.get(gid=task_gid)
        
        # Remove existing dependencies
        TaskDependency.objects.filter(successor=task).delete()
        
        # Add new dependencies
        for dep_gid in dependency_gids:
            dependency_task = Task.objects.get(gid=dep_gid)
            TaskDependency.objects.create(
                predecessor=dependency_task,
                successor=task
            )
        
        return task

    @transaction.atomic
    def remove_task_dependencies(self, task_gid: str, dependency_gids: List[str]) -> Task:
        """Remove specific dependencies from a task."""
        task = Task.objects.get(gid=task_gid)
        TaskDependency.objects.filter(
            successor=task,
            predecessor__gid__in=dependency_gids
        ).delete()
        return task

    def get_task_dependents(self, task_gid: str) -> List[Task]:
        """Get tasks that depend on this task (successors)."""
        task = Task.objects.get(gid=task_gid)
        dependents = TaskDependency.objects.filter(predecessor=task).select_related('successor')
        return [dep.successor for dep in dependents]

    @transaction.atomic
    def set_task_dependents(self, task_gid: str, dependent_gids: List[str]) -> Task:
        """Set dependents for a task (tasks that depend on this task)."""
        task = Task.objects.get(gid=task_gid)
        
        # Remove existing dependents
        TaskDependency.objects.filter(predecessor=task).delete()
        
        # Add new dependents
        for dep_gid in dependent_gids:
            dependent_task = Task.objects.get(gid=dep_gid)
            TaskDependency.objects.create(
                predecessor=task,
                successor=dependent_task
            )
        
        return task

    @transaction.atomic
    def remove_task_dependents(self, task_gid: str, dependent_gids: List[str]) -> Task:
        """Remove specific dependents from a task."""
        task = Task.objects.get(gid=task_gid)
        TaskDependency.objects.filter(
            predecessor=task,
            successor__gid__in=dependent_gids
        ).delete()
        return task

