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
    missing_field_error,
    invalid_field_error,
    server_error
)


class CreateSubtaskView(APIView):
    """
    Create a subtask for a task.
    Creates a new subtask and adds it to the parent task.
    Matches Asana API: POST /tasks/{task_gid}/subtasks
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The task to add a subtask to',
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
                            'name': {'type': 'string', 'description': 'Name of the subtask'},
                            'notes': {'type': 'string', 'description': 'Description/notes'},
                            'assignee': {'type': 'string', 'description': 'User GID to assign'},
                        },
                        'required': ['name']
                    }
                }
            }
        },
        responses={
            201: OpenApiResponse(
                description="Subtask created successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "task",
                                "name": "New Subtask",
                                "parent": {
                                    "gid": "67890",
                                    "resource_type": "task",
                                    "name": "Parent Task"
                                }
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Missing required field',
                        value={
                            "errors": [
                                {
                                    "message": "name: Missing input",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Parent task not found",
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
        summary="Create a subtask",
        description="Creates a new subtask and adds it to the parent task. Returns the full record of the newly created subtask.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request, task_gid: str):
        # Validate task GID format
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                invalid_gid_error("task_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if parent task exists
        try:
            parent_task = Task.objects.get(gid=task_gid)
        except Task.DoesNotExist:
            return Response(
                not_found_error("task", task_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get request data
        data = request.data.get('data', request.data)
        
        # Validate required fields
        name = data.get('name')
        if not name:
            return Response(
                missing_field_error("name"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(name, str) or len(name.strip()) == 0:
            return Response(
                invalid_field_error("name", "Must be a non-empty string"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create subtask
        try:
            subtask = Task.objects.create(
                name=name,
                workspace=parent_task.workspace,
                parent=parent_task,
                notes=data.get('notes', ''),
                resource_subtype=data.get('resource_subtype', 'default_task'),
            )
            
            # Update parent's num_subtasks
            parent_task.num_subtasks = Task.objects.filter(parent=parent_task).count()
            parent_task.save()
            
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'gid': str(subtask.gid),
            'resource_type': 'task',
            'name': subtask.name,
            'resource_subtype': subtask.resource_subtype,
            'completed': subtask.completed,
            'created_at': subtask.created_at.isoformat(),
            'parent': {
                'gid': str(parent_task.gid),
                'resource_type': 'task',
                'name': parent_task.name
            },
            'workspace': {
                'gid': str(subtask.workspace.gid),
                'resource_type': 'workspace',
                'name': subtask.workspace.name
            }
        }
        
        return Response({'data': response_data}, status=status.HTTP_201_CREATED)
