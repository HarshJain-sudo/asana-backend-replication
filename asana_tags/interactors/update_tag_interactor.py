"""
Interactor for updating a tag.
"""
from typing import Dict, Any, Optional
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tags.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tags.exceptions.custom_exceptions import (
    TagDoesNotExistException,
    TagAlreadyExistsException
)


class UpdateTagInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_tag(
        self,
        tag_gid: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        notes: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing tag.
        
        Args:
            tag_gid: Tag GID (required)
            name: Tag name (optional)
            color: Hex color code (optional)
            notes: Tag notes (optional)
        
        Returns:
            Dict containing updated tag response data
        """
        tag = self.storage.update_tag(
            tag_gid=tag_gid,
            name=name,
            color=color,
            notes=notes,
            **kwargs
        )
        
        if not tag:
            raise TagDoesNotExistException()
        
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

