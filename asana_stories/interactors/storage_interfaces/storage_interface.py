from abc import ABC, abstractmethod
from typing import List, Optional
from asana_stories.models.story import Story


class StorageInterface(ABC):
    @abstractmethod
    def get_story(self, story_gid: str) -> Optional[Story]:
        pass

    @abstractmethod
    def get_task_stories(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Story]:
        pass

