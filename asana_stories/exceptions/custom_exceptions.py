from asana_stories.constants.exception_messages import (
    STORY_DOES_NOT_EXIST,
    INVALID_STORY_GID,
)


class StoryDoesNotExistException(Exception):
    def __init__(self, message=STORY_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidStoryGidException(Exception):
    def __init__(self, message=INVALID_STORY_GID):
        self.message = message
        super().__init__(self.message)

