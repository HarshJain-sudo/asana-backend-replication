"""
API view for updating a workspace.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter
)
from asana_workspaces.interactors.update_workspace_interactor import (
    UpdateWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.presenters.get_workspace_presenter_implementation import (
    GetWorkspacePresenterImplementation
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_workspaces.serializers import (
    WorkspaceUpdateSerializer,
    WorkspaceSerializer
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class UpdateWorkspaceView(APIView):
    @ratelimit(key='ip', rate='5/s', method='PUT')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace.'
            )
        ],
        request=WorkspaceUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=WorkspaceSerializer,
                description="Workspace updated successfully."
            ),
            400: OpenApiResponse(
                description="Bad Request - Invalid input data."
            ),
            404: OpenApiResponse(
                description="Not Found - Workspace does not exist."
            ),
        },
        summary="Update a workspace",
        description="Updates an existing workspace."
    )
    def put(self, request, workspace_gid: str):
        try:
            validate_uuid(workspace_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WorkspaceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = StorageImplementation()
        presenter = GetWorkspacePresenterImplementation()
        interactor = UpdateWorkspaceInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.update_workspace_wrapper(
                workspace_gid=workspace_gid,
                name=serializer.validated_data.get('name'),
                is_organization=serializer.validated_data.get(
                    'is_organization'
                )
            )
            return Response(response, status=status.HTTP_200_OK)
        except WorkspaceDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Catch any other errors and return 500
            return Response(
                {'errors': [{
                    'message': f'Internal server error: {str(e)}',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

