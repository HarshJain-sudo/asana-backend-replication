from typing import Dict, Any, Optional
from asana_tags.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tags.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_tags.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetTagsInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_tags(
        self,
        workspace_gid: Optional[str] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        tags = self.storage.get_tags(
            workspace_gid=workspace_gid,
            offset=offset,
            limit=limit
        )

        tags_list = [
            {
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
            for tag in tags
        ]

        return self.presenter.get_tags_response(tags_list)

