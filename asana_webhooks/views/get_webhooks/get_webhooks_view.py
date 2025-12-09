from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_webhooks.interactors.get_webhooks_interactor import (
    GetWebhooksInteractor
)
from asana_webhooks.storages.storage_implementation import (
    StorageImplementation
)
from asana_webhooks.presenters.get_webhooks_presenter_implementation import (
    GetWebhooksPresenterImplementation
)
from asana_webhooks.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetWebhooksView(APIView):
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
            ),
            OpenApiParameter(
                name='resource',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by resource type (task, project, etc.)',
                required=False,
                examples=[
                    OpenApiExample('Task webhooks', value='task'),
                    OpenApiExample('Project webhooks', value='project')
                ]
            )
        ],
        responses={
            200: OpenApiResponse(
                description="List of webhooks retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "123e4567-e89b-12d3-a456-426614174000",
                                    "resource": "task",
                                    "resource_gid": "123e4567-e89b-12d3-a456-426614174001",
                                    "target": "https://example.com/webhook",
                                    "active": True,
                                    "created_at": "2025-12-09T10:00:00Z",
                                    "updated_at": "2025-12-09T10:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            )
        },
        summary="List all webhooks",
        description="""
        Retrieves a list of all registered webhooks.
        
        **Features:**
        - Pagination support
        - Filter by resource type
        - Shows active/inactive status
        
        **Resource Types:**
        - task
        - project
        - story
        - workspace
        """,
        tags=["Webhooks"]
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
        presenter = GetWebhooksPresenterImplementation()
        interactor = GetWebhooksInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_webhooks(
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)
