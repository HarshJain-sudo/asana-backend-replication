from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_workspaces.serializers import ErrorResponseSerializer
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
import hashlib
import time
import json


class GetWorkspaceEventsView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace or organization.',
                required=True
            ),
            OpenApiParameter(
                name='sync',
                type=str,
                location=OpenApiParameter.QUERY,
                description='A sync token received from the last request, or none on first sync.',
                required=False
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Provides "pretty" output.',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved events.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [],
                            "sync": "de4774f6915eae04714ca93bb2f5ee81",
                            "has_more": False
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
            412: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="The sync token is too old. A fresh sync token is included in the response."
            ),
        },
        summary="Get workspace events",
        description="Returns the full record for all events that have occurred since the sync token was created.",
        tags=["Workspaces"]
    )
    def get(self, request, workspace_gid: str):
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        sync_token = request.query_params.get('sync')
        
        try:
            validate_uuid(workspace_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'workspace: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        
        # Check if workspace exists
        workspace = storage.get_workspace(workspace_gid)
        if not workspace:
            error_response = {
                'errors': [{
                    'message': 'Workspace does not exist',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Get workspace events (for now, returns empty list as Events model is not implemented)
            events = storage.get_workspace_events(
                workspace_gid=workspace_gid,
                offset=0,
                limit=1000
            )
            
            # Generate sync token
            sync_token_new = hashlib.md5(
                f"{workspace_gid}_{int(time.time())}".encode()
            ).hexdigest()
            
            # Format events (empty for now)
            events_list = []
            
            response = {
                'data': events_list,
                'sync': sync_token_new,
                'has_more': False
            }
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_200_OK
                )
            
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

