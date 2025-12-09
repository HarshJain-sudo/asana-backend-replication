from typing import Dict, Any
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tags.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tags.exceptions.custom_exceptions import (
    TagDoesNotExistException
)


class GetTagInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_tag(self, tag_gid: str) -> Dict[str, Any]:
        tag = self.storage.get_tag(tag_gid)

        if not tag:
            raise TagDoesNotExistException()

        tag_dict = {
            'gid': str(tag.gid),
            'name': tag.name,
            'workspace': {
                'gid': str(tag.workspace.gid),
                'name': tag.workspace.name
            },
            'color': tag.color,
            'created_at': tag.created_at.isoformat(),
            'updated_at': tag.updated_at.isoformat(),
        }

        return self.presenter.get_tag_response(tag_dict)

