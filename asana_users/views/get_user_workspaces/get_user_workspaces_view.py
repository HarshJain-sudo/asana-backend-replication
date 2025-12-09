"""
API view for retrieving user workspaces.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_users.interactors.get_user_workspaces_interactor import (
    GetUserWorkspacesInteractor
)
from asana_users.storages.storage_implementation import (
    StorageImplementation
)
from asana_users.presenters.get_user_presenter_implementation import (
    GetUserPresenterImplementation
)
from asana_users.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)
from asana_backend.utils.validators import (
    validate_uuid,
    validate_pagination_params
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetUserWorkspacesView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    def get(self, request, user_gid: str):
        # Validate UUID format
        try:
            validate_uuid(user_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid user GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and normalize pagination params
        offset, limit = validate_pagination_params(
            offset=request.query_params.get('offset'),
            limit=request.query_params.get('limit'),
            max_limit=MAX_LIMIT
        )

        storage = StorageImplementation()
        presenter = GetUserPresenterImplementation()
        interactor = GetUserWorkspacesInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_user_workspaces(
                user_gid=user_gid,
                offset=offset,
                limit=limit
            )
            return Response(response, status=status.HTTP_200_OK)
        except UserDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

