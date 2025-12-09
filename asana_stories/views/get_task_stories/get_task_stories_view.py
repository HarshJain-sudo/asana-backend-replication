from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_stories.interactors.get_task_stories_interactor import (
    GetTaskStoriesInteractor
)
from asana_stories.storages.storage_implementation import (
    StorageImplementation
)
from asana_stories.presenters.get_task_stories_presenter_implementation import (
    GetTaskStoriesPresenterImplementation
)
from asana_stories.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import (
    validate_uuid,
    validate_pagination_params
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTaskStoriesView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, task_gid: str):
        # Validate UUID format
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and normalize pagination params
        offset, limit = validate_pagination_params(
            offset=request.query_params.get('offset'),
            limit=request.query_params.get('limit'),
            max_limit=MAX_LIMIT
        )

        storage = StorageImplementation()
        presenter = GetTaskStoriesPresenterImplementation()
        interactor = GetTaskStoriesInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_task_stories(
            task_gid=task_gid,
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)

