from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_tags.interactors.get_workspace_tags_interactor import (
    GetWorkspaceTagsInteractor
)
from asana_tags.storages.storage_implementation import (
    StorageImplementation
)
from asana_tags.presenters.get_tags_presenter_implementation import (
    GetTagsPresenterImplementation
)
from asana_tags.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import (
    validate_uuid,
    validate_pagination_params
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetWorkspaceTagsView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, workspace_gid: str):
        # Validate UUID format
        try:
            validate_uuid(workspace_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid workspace GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and normalize pagination params
        offset, limit = validate_pagination_params(
            offset=request.query_params.get('offset'),
            limit=request.query_params.get('limit'),
            max_limit=MAX_LIMIT
        )

        storage = StorageImplementation()
        presenter = GetTagsPresenterImplementation()
        interactor = GetWorkspaceTagsInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_workspace_tags(
            workspace_gid=workspace_gid,
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)

