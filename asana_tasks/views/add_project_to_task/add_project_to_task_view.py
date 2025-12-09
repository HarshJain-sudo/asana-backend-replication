from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_tasks.interactors.add_project_to_task_interactor import (
    AddProjectToTaskInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.serializers import TaskProjectSerializer
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class AddProjectToTaskView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='UUID of the task',
                required=True
            )
        ],
        request=TaskProjectSerializer,
        responses={
            200: OpenApiResponse(
                description="Project added to task successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "123e4567-e89b-12d3-a456-426614174000",
                                "name": "Build Asana Clone"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Task or Project not found")
        },
        summary="Add project to task",
        description="Associates a task with a project. A task can belong to multiple projects.",
        tags=["Tasks - Relationships"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': [{'message': str(serializer.errors)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = AddProjectToTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.add_project_to_task(
                task_gid,
                str(serializer.validated_data['project_gid'])
            )
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )
