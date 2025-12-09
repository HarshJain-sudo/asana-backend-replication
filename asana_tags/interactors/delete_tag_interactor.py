"""
Interactor for deleting a tag.
"""
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tags.exceptions.custom_exceptions import (
    TagDoesNotExistException
)


class DeleteTagInteractor:
    def __init__(
        self,
        storage: StorageInterface
    ):
        self.storage = storage

    def delete_tag(
        self,
        tag_gid: str
    ) -> None:
        """
        Delete a tag.
        
        Args:
            tag_gid: Tag GID (required)
        """
        success = self.storage.delete_tag(tag_gid)
        
        if not success:
            raise TagDoesNotExistException()

