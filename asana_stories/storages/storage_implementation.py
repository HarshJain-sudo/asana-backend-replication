from typing import List, Optional
from asana_stories.models.story import Story
from asana_stories.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_story(self, story_gid: str) -> Optional[Story]:
        try:
            return Story.objects.get(gid=story_gid)
        except Story.DoesNotExist:
            return None

    def get_task_stories(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Story]:
        return list(
            Story.objects.filter(
                task__gid=task_gid
            ).order_by('-created_at')[offset:offset + limit]
        )

