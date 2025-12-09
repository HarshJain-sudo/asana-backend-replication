"""
API view for creating a workspace.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)
from asana_workspaces.interactors.create_workspace_interactor import (
    CreateWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.presenters.get_workspace_presenter_implementation import (
    GetWorkspacePresenterImplementation
)
from asana_workspaces.serializers import (
    WorkspaceCreateSerializer,
    WorkspaceSerializer
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class CreateWorkspaceView(APIView):
    @ratelimit(key='ip', rate='5/m', method='POST')
    @extend_schema(
        request=WorkspaceCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=WorkspaceSerializer,
                description="Workspace created successfully."
            ),
            400: OpenApiResponse(
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

