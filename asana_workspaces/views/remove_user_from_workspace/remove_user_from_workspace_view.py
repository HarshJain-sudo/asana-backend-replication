from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_workspaces.interactors.remove_user_from_workspace_interactor import (
    RemoveUserFromWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.serializers import (
    WorkspaceRemoveUserRequestSerializer,
    ErrorResponseSerializer
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class RemoveUserFromWorkspaceView(APIView):
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
        ],
        request=WorkspaceRemoveUserRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="The user was removed successfully to the workspace or organization.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={"data": {}}
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
        summary="Remove a user from a workspace or organization",
        description="Remove a user from a workspace or organization. The user making this call must be an admin in the workspace.",
        tags=["Workspaces"]
    )
    def post(self, request, workspace_gid: str):
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
        
        serializer = WorkspaceRemoveUserRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"user: {str(serializer.errors)}",
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        interactor = RemoveUserFromWorkspaceInteractor(storage=storage)
        
        try:
            interactor.remove_user_from_workspace(
                workspace_gid=workspace_gid,
                user=serializer.validated_data['user']
            )
            return Response({'data': {}}, status=status.HTTP_200_OK)
        except (WorkspaceDoesNotExistException, UserDoesNotExistException) as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

