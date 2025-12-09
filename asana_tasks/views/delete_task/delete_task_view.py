from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from asana_tasks.interactors.delete_task_interactor import (
    DeleteTaskInteractor
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


class DeleteTaskView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='UUID of the task to delete',
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                description="Task deleted successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={"data": {}}
                    )
                ]
            ),
            400: OpenApiResponse(description="Invalid UUID format"),
            404: OpenApiResponse(description="Task not found")
        },
        summary="Delete a task",
        description="Permanently deletes a task. This action cannot be undone.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='DELETE')
    def delete(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = DeleteTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.delete_task(task_gid)
            return Response(response, status=status.HTTP_200_OK)
        except TaskDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
