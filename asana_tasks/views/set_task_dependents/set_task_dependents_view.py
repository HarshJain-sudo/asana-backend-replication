from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from asana_tasks.interactors.set_task_dependents_interactor import SetTaskDependentsInteractor
from asana_tasks.storages.storage_implementation import StorageImplementation
from asana_tasks.presenters.get_task_presenter_implementation import GetTaskPresenterImplementation
from asana_tasks.exceptions.custom_exceptions import TaskDoesNotExistException
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_tasks.serializers import TaskSingleResponseSerializer, ErrorResponseSerializer
from asana_backend.utils.error_messages import invalid_gid_error, not_found_error


class SetTaskDependentsView(APIView):
    @ratelimit(key='ip', rate='5/s', method='POST')
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
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'dependents': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'List of task GIDs that depend on this task'
                            }
                        }
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                response=TaskSingleResponseSerializer,
                description="Task dependents set successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid task GID format or dependent GIDs."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found - Task or dependent task does not exist."
            ),
        },
        summary="Set task dependents",
        description="Sets the tasks that depend on this task.",
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

        data = request.data.get('data', request.data)
        dependent_gids = data.get('dependents', [])

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = SetTaskDependentsInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.set_task_dependents(task_gid, dependent_gids)
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

