"""
API view for deleting a workspace.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter
)
from asana_workspaces.interactors.delete_workspace_interactor import (
    DeleteWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class DeleteWorkspaceView(APIView):
    @ratelimit(key='ip', rate='5/s', method='DELETE')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace.'
            )
        ],
        responses={
            204: OpenApiResponse(
                response=None,
                description="Workspace deleted successfully."
            ),
            400: OpenApiResponse(
                description="Bad Request - Invalid workspace GID format."
            ),
            404: OpenApiResponse(
                description="Not Found - Workspace does not exist."
            ),
        },
        summary="Delete a workspace",
        description="Deletes an existing workspace."
    )
    def delete(self, request, workspace_gid: str):
        try:
            validate_uuid(workspace_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        interactor = DeleteWorkspaceInteractor(storage=storage)

        try:
            interactor.delete_workspace_wrapper(workspace_gid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WorkspaceDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

