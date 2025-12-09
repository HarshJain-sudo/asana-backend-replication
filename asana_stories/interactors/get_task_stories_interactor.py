from typing import Dict, Any
from asana_stories.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_stories.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_stories.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetTaskStoriesInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_task_stories(
        self,
        task_gid: str,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        stories = self.storage.get_task_stories(
            task_gid=task_gid,
            offset=offset,
            limit=limit
        )

        stories_list = [
            {
                'gid': str(story.gid),
                'task': {
                    'gid': str(story.task.gid),
                    'name': story.task.name
                },
                'text': story.text,
                'html_text': story.html_text,
                'type': story.type,
                'is_pinned': story.is_pinned,
                'created_at': story.created_at.isoformat(),
                'created_by': {
                    'gid': str(story.created_by.gid),
                    'name': story.created_by.name
                } if story.created_by else None,
            }
            for story in stories
        ]

        return self.presenter.get_stories_response(stories_list)

