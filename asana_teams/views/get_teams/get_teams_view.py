from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_teams.interactors.get_teams_interactor import (
    GetTeamsInteractor
)
from asana_teams.storages.storage_implementation import (
    StorageImplementation
)
from asana_teams.presenters.get_teams_presenter_implementation import (
    GetTeamsPresenterImplementation
)
from asana_teams.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTeamsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='offset',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Offset for pagination (default: 0)',
                required=False
            ),
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Number of results (default: 50, max: 100)',
                required=False
            )
        ],
        responses={
            200: OpenApiResponse(
                description="List of teams retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "123e4567-e89b-12d3-a456-426614174000",
                                    "name": "Engineering Team",
                                    "description": "Backend development team",
                                    "workspace": {
                                        "gid": "123e4567-e89b-12d3-a456-426614174001",
                                        "name": "My Workspace"
                                    },
                                    "created_at": "2025-12-09T10:00:00Z",
                                    "updated_at": "2025-12-09T10:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            )
        },
        summary="List all teams",
        description="""
        Retrieves a list of all teams across all workspaces.
        
        **Features:**
        - Pagination support
        - Returns team details with workspace info
        """,
        tags=["Teams"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request):
        try:
            offset, limit = validate_pagination_params(
                offset=request.query_params.get('offset'),
            limit=request.query_params.get('limit'),
                max_limit=MAX_LIMIT
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTeamsPresenterImplementation()
        interactor = GetTeamsInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_teams(
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)
