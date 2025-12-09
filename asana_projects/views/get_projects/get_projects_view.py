from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_projects.interactors.get_projects_interactor import (
    GetProjectsInteractor
)
from asana_projects.storages.storage_implementation import (
    StorageImplementation
)
from asana_projects.presenters.get_projects_presenter_implementation import (
    GetProjectsPresenterImplementation
)
from asana_projects.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetProjectsView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request):
        # Validate and normalize pagination params
        try:
            # Handle offset - can be int or string token
            offset_param = request.query_params.get('offset', '0')
            try:
                offset = int(offset_param)
            except ValueError:
                # If it's a token, treat as 0 for now
                offset = 0
            
            limit_param = request.query_params.get('limit')
            limit = int(limit_param) if limit_param else DEFAULT_LIMIT
            
            offset, limit = validate_pagination_params(
                offset=offset,
                limit=limit,
                max_limit=MAX_LIMIT
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional filters (matching API spec parameter names)
        workspace = request.query_params.get('workspace')
        team = request.query_params.get('team')
        archived = request.query_params.get('archived')
        opt_fields = request.query_params.get('opt_fields')

        # Convert archived to boolean if provided
        if archived is not None:
            archived = archived.lower() == 'true'

        storage = StorageImplementation()
        presenter = GetProjectsPresenterImplementation()
        interactor = GetProjectsInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_projects(
            workspace=workspace,
            team=team,
            archived=archived,
            opt_fields=opt_fields,
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)

