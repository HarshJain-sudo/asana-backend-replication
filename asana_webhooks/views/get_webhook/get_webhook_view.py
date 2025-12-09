from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_webhooks.interactors.get_webhook_interactor import (
    GetWebhookInteractor
)
from asana_webhooks.storages.storage_implementation import (
    StorageImplementation
)
from asana_webhooks.presenters.get_webhook_presenter_implementation import (
    GetWebhookPresenterImplementation
)
from asana_webhooks.exceptions.custom_exceptions import (
    WebhookDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetWebhookView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='webhook_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='UUID of the webhook',
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                description="Webhook retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "123e4567-e89b-12d3-a456-426614174000",
                                "resource": "task",
                                "resource_gid": "123e4567-e89b-12d3-a456-426614174001",
                                "target": "https://example.com/webhook",
                                "active": True,
                                "secret": "webhook_secret_key",
                                "created_at": "2025-12-09T10:00:00Z",
                                "updated_at": "2025-12-09T10:00:00Z"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Invalid UUID format"),
            404: OpenApiResponse(description="Webhook not found")
        },
        summary="Get a single webhook",
        description="""
        Retrieves detailed information about a specific webhook by UUID.
        
        **Returns:**
        - Webhook configuration
        - Target URL
        - Resource details
        - Active status
        - Secret for verification
        """,
        tags=["Webhooks"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, webhook_gid: str):
        try:
            validate_uuid(webhook_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid webhook GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetWebhookPresenterImplementation()
        interactor = GetWebhookInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_webhook(webhook_gid)
            return Response(response, status=status.HTTP_200_OK)
        except WebhookDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
