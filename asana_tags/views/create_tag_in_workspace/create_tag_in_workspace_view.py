from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_tags.interactors.create_tag_interactor import (
    CreateTagInteractor
)
from asana_tags.storages.storage_implementation import (
    StorageImplementation
)
from asana_tags.presenters.get_tag_presenter_implementation import (
    GetTagPresenterImplementation
)
from asana_tags.serializers import (
    TagCreateTagForWorkspaceRequestSerializer,
    TagSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_tags.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException,
    TagAlreadyExistsException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class CreateTagInWorkspaceView(APIView):
    @ratelimit(key='ip', rate='5/m', method='POST')
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
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default.',
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
        request=TagCreateTagForWorkspaceRequestSerializer,
        responses={
            201: OpenApiResponse(
                response=TagSingleResponseSerializer,
                description="Successfully created the newly specified tag.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "tag",
                                "name": "Important",
                                "color": "#ff0000",
                                "workspace": {
                                    "gid": "98765",
                                    "resource_type": "workspace",
                                    "name": "My Workspace"
                                }
                            }
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
        },
        summary="Create a tag in a workspace",
        description="Creates a new tag in a workspace or organization.",
        tags=["Tags"]
    )
    def post(self, request, workspace_gid: str):
        import json
        
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
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
        
        serializer = TagCreateTagForWorkspaceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"tag: {str(serializer.errors)}",
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        storage = StorageImplementation()
        presenter = GetTagPresenterImplementation()
        interactor = CreateTagInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            # Add workspace_gid to validated data
            validated_data = serializer.validated_data.copy()
            validated_data['workspace'] = workspace_gid
            
            response = interactor.create_tag(**validated_data)
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_201_CREATED
                )
            
            return Response(response, status=status.HTTP_201_CREATED)
        except (WorkspaceDoesNotExistException, TagAlreadyExistsException) as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            status_code = status.HTTP_404_NOT_FOUND if isinstance(e, WorkspaceDoesNotExistException) else status.HTTP_400_BAD_REQUEST
            return Response(error_response, status=status_code)
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

