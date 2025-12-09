from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_tasks.interactors.update_task_interactor import (
    UpdateTaskInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.serializers import TaskUpdateSerializer
from asana_tasks.exceptions.custom_exceptions import (
    TaskDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class UpdateTaskView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='UUID of the task to update',
                required=True
            )
        ],
        request=TaskUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Task updated successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "123e4567-e89b-12d3-a456-426614174000",
                                "name": "Updated Task Name",
                                "workspace": {
                                    "gid": "123e4567-e89b-12d3-a456-426614174001",
                                    "name": "My Workspace"
                                },
                                "assignee": {
                                    "gid": "123e4567-e89b-12d3-a456-426614174002",
                                    "name": "Jane Smith"
                                },
                                "assignee_status": "later",
                                "completed": True,
                                "completed_at": "2025-12-09T12:00:00Z",
                                "due_on": "2025-12-31",
                                "notes": "Updated notes",
                                "created_at": "2025-12-09T10:00:00Z",
                                "updated_at": "2025-12-09T12:00:00Z"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Task not found")
        },
        summary="Update a task",
        description="Updates an existing task. All fields are optional.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='PUT')
    def put(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': [{'message': str(serializer.errors)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = UpdateTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.update_task(task_gid, **serializer.validated_data)
            return Response(response, status=status.HTTP_200_OK)
        except TaskDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
