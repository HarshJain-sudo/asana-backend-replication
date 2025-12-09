"""
View for getting all workspaces and creating a new workspace.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_workspaces.interactors.get_workspaces_interactor import (
    GetWorkspacesInteractor
)
from asana_workspaces.interactors.create_workspace_interactor import (
    CreateWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.presenters.get_workspaces_presenter_implementation import (
    GetWorkspacesPresenterImplementation
)
from asana_workspaces.presenters.get_workspace_presenter_implementation import (
    GetWorkspacePresenterImplementation
)
from asana_workspaces.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_workspaces.serializers import (
    WorkspaceCreateSerializer,
    WorkspaceListResponseSerializer,
    WorkspaceSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetWorkspacesView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Results per page. The number of objects to return per page. The value must be between 1 and 100.',
                required=False,
                examples=[OpenApiExample('Default limit', value=50)]
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. Note: You can only pass in an offset that was returned to you via a previously paginated request.',
                required=False,
                examples=[OpenApiExample('Offset token', value='eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9')]
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False,
                examples=[
                    OpenApiExample(
                        'Include all optional fields',
                        value='email_domains,is_organization,name,offset,path,uri'
                    )
                ]
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Provides "pretty" output. Provides the response in a "pretty" format. In the case of JSON this means doing proper line breaking and indentation to make it readable.',
                required=False,
                examples=[OpenApiExample('Pretty output', value=True)]
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=WorkspaceListResponseSerializer,
                description="Return all workspaces visible to the authorized user.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "workspace",
                                    "name": "My Company Workspace"
                                }
                            ],
                            "next_page": {
                                "offset": "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9",
                                "path": "/workspaces?limit=50&offset=eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9",
                                "uri": "https://app.asana.com/api/1.0/workspaces?limit=50&offset=eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={
                            "errors": [
                                {
                                    "message": "limit: Invalid value",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors",
                                    "phrase": "6 sad squid snuggle softly"
                                }
                            ]
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="A valid authentication token was not provided with the request, so the API could not associate a user with the request."
            ),
            403: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
            500: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="There was a problem on Asana's end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error."
            ),
        },
        summary="Get multiple workspaces",
        description="Returns the compact records for all workspaces visible to the authorized user."
    )
    def get(self, request):
        import json
        import base64
        
        # Get query parameters
        opt_fields = request.query_params.get('opt_fields')
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
        # Handle offset - can be string token or integer
        offset_param = request.query_params.get('offset')
        if offset_param:
            try:
                # Try to decode if it's a base64 token
                try:
                    decoded = base64.b64decode(offset_param).decode('utf-8')
                    # If it decodes successfully, treat as token
                    offset = offset_param
                except:
                    # If not base64, try as integer
                    offset = int(offset_param)
            except ValueError:
                error_response = {
                    'errors': [{
                        'message': 'offset: Invalid format',
                        'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                        'phrase': '6 sad squid snuggle softly'
                    }]
                }
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            offset = 0
        
        # Validate limit
        limit_param = request.query_params.get('limit')
        try:
            if limit_param:
                limit = int(limit_param)
                if limit < 1 or limit > MAX_LIMIT:
                    raise ValueError(f"Limit must be between 1 and {MAX_LIMIT}")
            else:
                limit = DEFAULT_LIMIT
        except ValueError as e:
            error_response = {
                'errors': [{
                    'message': f'limit: {str(e)}',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        storage = StorageImplementation()
        presenter = GetWorkspacesPresenterImplementation()
        interactor = GetWorkspacesInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            # Convert offset to int if it's a number (for storage)
            offset_int = offset if isinstance(offset, int) else 0
            
            response = interactor.get_workspaces(
                offset=offset_int,
                limit=limit,
                opt_fields=opt_fields,
                request=request  # Pass request for generating next_page URLs
            )
            
            # Handle opt_pretty for pretty JSON formatting
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

    @ratelimit(key='ip', rate='5/m', method='POST')
    @extend_schema(
        request=WorkspaceCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=WorkspaceSingleResponseSerializer,
                description="Workspace created successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid input data."
            ),
        },
        summary="Create a new workspace",
        description="Creates a new workspace."
    )
    def post(self, request):
        serializer = WorkspaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = StorageImplementation()
        presenter = GetWorkspacePresenterImplementation()
        interactor = CreateWorkspaceInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.create_workspace_wrapper(
            name=serializer.validated_data['name'],
            is_organization=serializer.validated_data.get(
                'is_organization',
                False
            )
        )

        return Response(response, status=status.HTTP_201_CREATED)

