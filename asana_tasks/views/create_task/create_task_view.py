from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from asana_tasks.interactors.create_task_interactor import (
    CreateTaskInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.serializers import (
    TaskSerializer,
    TaskCreateRequestSerializer,
    TaskSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class CreateTaskView(APIView):
    @extend_schema(
        request=TaskCreateRequestSerializer,
        responses={
            201: OpenApiResponse(
                response=TaskSingleResponseSerializer,
                description="Task created successfully.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "1234567890123456",
                                "resource_type": "task",
                                "name": "New Task",
                                "workspace": {
                                    "gid": "9876543210987654",
                                    "resource_type": "workspace",
                                    "name": "My Workspace"
                                },
                                "assignee": None,
                                "completed": False,
                                "created_at": "2024-01-01T00:00:00Z",
                                "modified_at": "2024-01-01T00:00:00Z"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid input data."
            )
        },
        summary="Create a new task",
        description="Creates a new task in the specified workspace. Requires task name and workspace GID.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request):
        # Try new API spec format first
        serializer = TaskCreateRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Fallback to legacy format
            legacy_serializer = TaskSerializer(data=request.data)
            if legacy_serializer.is_valid():
                serializer = legacy_serializer
            else:
                return Response(
                    {'errors': [{'message': str(serializer.errors)}]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = CreateTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            # Convert validated data to interactor format
            validated_data = serializer.validated_data.copy()
            
            # Handle both formats
            if 'workspace' in validated_data:
                validated_data['workspace'] = validated_data['workspace']
            elif 'workspace_gid' in validated_data:
                validated_data['workspace'] = str(validated_data['workspace_gid'])
            
            if 'assignee' in validated_data and validated_data['assignee']:
                validated_data['assignee'] = validated_data['assignee']
            elif 'assignee_gid' in validated_data:
                validated_data['assignee'] = str(validated_data['assignee_gid']) if validated_data['assignee_gid'] else None
            
            response = interactor.create_task(**validated_data)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
