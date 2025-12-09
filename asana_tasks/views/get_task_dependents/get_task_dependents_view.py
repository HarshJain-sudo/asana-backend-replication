from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from asana_tasks.interactors.get_task_dependents_interactor import GetTaskDependentsInteractor
from asana_tasks.storages.storage_implementation import StorageImplementation
from asana_tasks.presenters.get_tasks_presenter_implementation import GetTasksPresenterImplementation
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_tasks.serializers import TaskListResponseSerializer, ErrorResponseSerializer
from asana_backend.utils.error_messages import invalid_gid_error, not_found_error


class GetTaskDependentsView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the task.',
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=TaskListResponseSerializer,
                description="List of tasks that depend on this task."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid task GID format."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found - Task does not exist."
            ),
        },
        summary="Get task dependents",
        description="Returns the tasks that depend on this task.",
        tags=["Tasks"]
    )
    def get(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                invalid_gid_error("task_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTasksPresenterImplementation()
        interactor = GetTaskDependentsInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_task_dependents(task_gid)
            return Response(response, status=status.HTTP_200_OK)
        except TaskDoesNotExistException as e:
            return Response(
                not_found_error("task", task_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

