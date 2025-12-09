from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_stories.interactors.get_story_interactor import (
    GetStoryInteractor
)
from asana_stories.storages.storage_implementation import (
    StorageImplementation
)
from asana_stories.presenters.get_story_presenter_implementation import (
    GetStoryPresenterImplementation
)
from asana_stories.exceptions.custom_exceptions import (
    StoryDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetStoryView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, story_gid: str):
        # Validate UUID format
        try:
            validate_uuid(story_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid story GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetStoryPresenterImplementation()
        interactor = GetStoryInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_story(story_gid)
            return Response(response, status=status.HTTP_200_OK)
        except StoryDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

