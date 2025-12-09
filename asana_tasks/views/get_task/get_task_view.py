from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_tasks.interactors.get_task_interactor import (
    GetTaskInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.exceptions.custom_exceptions import (
    TaskDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTaskView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='UUID of the task',
                required=True,
                examples=[
                    OpenApiExample(
                        'Example UUID',
                        value='123e4567-e89b-12d3-a456-426614174000'
                    )
                ]
            )
        ],
        responses={
            200: OpenApiResponse(
                description="Task retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "123e4567-e89b-12d3-a456-426614174000",
                                "name": "Build Asana Clone",
                                "workspace": {
                                    "gid": "123e4567-e89b-12d3-a456-426614174001",
                                    "name": "My Workspace"
                                },
                                "assignee": {
                                    "gid": "123e4567-e89b-12d3-a456-426614174002",
                                    "name": "John Doe"
                                },
                                "assignee_status": "today",
                                "completed": False,
                                "completed_at": None,
                                "due_on": "2025-12-31",
                                "due_at": None,
                                "notes": "Complete all endpoints",
                                "created_at": "2025-12-09T10:00:00Z",
                                "updated_at": "2025-12-09T10:00:00Z"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid UUID format",
                examples=[
                    OpenApiExample(
                        'Error Response',
                        value={
                            "errors": [
                                {"message": "Invalid task GID format"}
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Task not found",
                examples=[
                    OpenApiExample(
                        'Error Response',
                        value={
                            "errors": [
                                {"message": "Task does not exist"}
                            ]
                        }
                    )
                ]
            )
        },
        summary="Get a single task",
        description="Retrieves detailed information about a specific task by its UUID.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = GetTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_task(task_gid)
            return Response(response, status=status.HTTP_200_OK)
        except TaskDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
