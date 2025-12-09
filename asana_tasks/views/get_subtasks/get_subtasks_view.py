from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_tasks.models.task import Task
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    invalid_field_error
)


class GetSubtasksView(APIView):
    """
    Get subtasks from a task.
    Returns a compact representation of all subtasks of a task.
    Matches Asana API: GET /tasks/{task_gid}/subtasks
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The task to get subtasks from',
                required=True
            ),
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Results per page (1-100)',
                required=False
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token for pagination',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved subtasks",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "task",
                                    "name": "Subtask 1"
                                }
                            ]
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={
                            "errors": [
                                {
                                    "message": "task_gid: Invalid GID format",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Task not found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "task: Unknown object: 12345",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    )
                ]
            ),
        },
        summary="Get subtasks from a task",
        description="Returns a compact representation of all of the subtasks of a task.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, task_gid: str):
        # Validate task GID format
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                invalid_gid_error("task_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if task exists
        try:
            task = Task.objects.get(gid=task_gid)
        except Task.DoesNotExist:
            return Response(
                not_found_error("task", task_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get pagination params
        try:
            limit = int(request.query_params.get('limit', 50))
            if limit < 1 or limit > 100:
                return Response(
                    invalid_field_error("limit", "Value must be between 1 and 100"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                invalid_field_error("limit", "Must be a valid integer"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get subtasks
        subtasks = Task.objects.filter(parent=task)[:limit]
        
        subtasks_list = [
            {
                'gid': str(subtask.gid),
                'resource_type': 'task',
                'name': subtask.name,
                'resource_subtype': subtask.resource_subtype,
                'completed': subtask.completed,
            }
            for subtask in subtasks
        ]
        
        return Response({'data': subtasks_list}, status=status.HTTP_200_OK)
