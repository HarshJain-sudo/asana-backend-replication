from typing import Dict, Any
from asana_stories.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_stories.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_stories.exceptions.custom_exceptions import (
    StoryDoesNotExistException
)


class GetStoryInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_story(self, story_gid: str) -> Dict[str, Any]:
        story = self.storage.get_story(story_gid)

        if not story:
            raise StoryDoesNotExistException()

        story_dict = {
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

        return self.presenter.get_story_response(story_dict)

