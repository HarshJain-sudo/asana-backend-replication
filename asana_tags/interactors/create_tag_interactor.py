"""
Interactor for creating a tag.
"""
from typing import Dict, Any, List, Optional
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tags.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tags.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException,
    TagAlreadyExistsException
)


class CreateTagInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_tag(
        self,
        name: str,
        workspace: str,
        color: Optional[str] = None,
        notes: Optional[str] = None,
        followers: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new tag.
        
        Args:
            name: Tag name (required)
            workspace: Workspace GID (required)
            color: Hex color code (optional)
            notes: Tag notes (optional)
            followers: List of user identifiers (optional)
        
        Returns:
            Dict containing tag response data
        """
        tag = self.storage.create_tag(
            name=name,
            workspace_gid=workspace,
            color=color,
            notes=notes,
            **kwargs
        )
        
        # Handle followers if provided (would need TagFollower model)
        # For now, skipping follower implementation
        
        # Format response matching TagResponse schema
        tag_dict = {
            'gid': str(tag.gid),
            'resource_type': 'tag',
            'name': tag.name,
            'color': tag.color,
            'workspace': {
                'gid': str(tag.workspace.gid),
                'resource_type': 'workspace',
                'name': tag.workspace.name
            },
            'created_at': tag.created_at.isoformat(),
            'followers': [],  # Not implemented yet
        }
        
        return self.presenter.get_tag_response(tag_dict)

