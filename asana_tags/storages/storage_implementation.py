from typing import List, Optional
from asana_tags.models.tag import Tag
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_tag(self, tag_gid: str) -> Optional[Tag]:
        try:
            return Tag.objects.get(gid=tag_gid)
        except Tag.DoesNotExist:
            return None

    def get_tags(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        queryset = Tag.objects.all()

        if workspace_gid:
            queryset = queryset.filter(workspace__gid=workspace_gid)

        return list(queryset[offset:offset + limit])

    def get_workspace_tags(
        self,
        workspace_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        return list(
            Tag.objects.filter(
                workspace__gid=workspace_gid
            )[offset:offset + limit]
        )
    
    def create_tag(
        self,
        name: str,
        workspace_gid: str,
        color: str = None,
        notes: str = None,
        **kwargs
    ) -> Tag:
        from asana_workspaces.models.workspace import Workspace
        from asana_tags.exceptions.custom_exceptions import (
            WorkspaceDoesNotExistException,
            TagAlreadyExistsException
        )
        
        try:
            workspace = Workspace.objects.get(gid=workspace_gid)
        except Workspace.DoesNotExist:
            raise WorkspaceDoesNotExistException()
        
        # Check for duplicate tag name in workspace
        if Tag.objects.filter(workspace=workspace, name=name).exists():
            raise TagAlreadyExistsException(
                f"Tag with name '{name}' already exists in workspace '{workspace_gid}'"
            )
        
        tag = Tag.objects.create(
            name=name,
            workspace=workspace,
            color=color,
            **kwargs
        )
        return tag
    
    def update_tag(
        self,
        tag_gid: str,
        name: str = None,
        color: str = None,
        notes: str = None,
        **kwargs
    ) -> Tag:
        from asana_tags.exceptions.custom_exceptions import (
            TagAlreadyExistsException
        )
        
        tag = self.get_tag(tag_gid)
        if not tag:
            return None
        
        # Check for duplicate name if name is being updated
        if name is not None and name != tag.name:
            if Tag.objects.filter(workspace=tag.workspace, name=name).exclude(gid=tag.gid).exists():
                raise TagAlreadyExistsException(
                    f"Tag with name '{name}' already exists in workspace '{tag.workspace.gid}'"
                )
            tag.name = name
        
        if color is not None:
            tag.color = color
        
        for key, value in kwargs.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        
        tag.save()
        return tag
    
    def delete_tag(
        self,
        tag_gid: str
    ) -> bool:
        tag = self.get_tag(tag_gid)
        if not tag:
            return False
        
        tag.delete()
        return True
    
    def get_task_tags(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Tag]:
        from asana_tasks.models.task_tag import TaskTag
        from asana_tasks.models.task import Task
        from asana_tasks.exceptions.custom_exceptions import (
            TaskDoesNotExistException
        )
        
        try:
            task = Task.objects.get(gid=task_gid)
        except Task.DoesNotExist:
            raise TaskDoesNotExistException()
        
        task_tags = TaskTag.objects.filter(
            task=task
        ).select_related('tag')[offset:offset + limit]
        
        return [task_tag.tag for task_tag in task_tags]

