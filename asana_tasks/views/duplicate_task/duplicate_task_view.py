from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_tasks.storages.storage_implementation import StorageImplementation
from asana_tasks.presenters.get_task_presenter_implementation import GetTaskPresenterImplementation
from asana_tasks.interactors.duplicate_task_interactor import DuplicateTaskInteractor
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_tasks.serializers import TaskSingleResponseSerializer, ErrorResponseSerializer
from asana_backend.utils.error_messages import invalid_gid_error, not_found_error


class DuplicateTaskView(APIView):
    @ratelimit(key='ip', rate='5/s', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the task to duplicate.',
                required=True
            ),
        ],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string', 'description': 'Name of the new task'},
                            'include': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Elements to duplicate (notes, assignee, subtasks, attachments, etc.)'
                            },
                        }
                    }
                }
            }
        },
        responses={
            201: OpenApiResponse(
                response=TaskSingleResponseSerializer,
                description="Task duplicated successfully."
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
        summary="Duplicate a task",
        description="Creates a copy of an existing task with a new name.",
        tags=["Tasks"]
    )
    def post(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                invalid_gid_error("task_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = DuplicateTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        # Get request data
        data = request.data.get('data', request.data)
        name = data.get('name')
        include = data.get('include', [])

        try:
            response = interactor.duplicate_task(
                task_gid=task_gid,
                name=name,
                include=include
            )
            return Response(response, status=status.HTTP_201_CREATED)
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

