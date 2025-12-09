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
    bad_request_error
)


class SetParentView(APIView):
    """
    Set the parent of a task.
    Changes the parent of a task. A parent can be null for top-level tasks.
    Matches Asana API: POST /tasks/{task_gid}/setParent
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='task_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The task to set parent for',
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
                            'parent': {'type': 'string', 'description': 'The new parent task GID, or null for no parent'},
                            'insert_after': {'type': 'string', 'description': 'A subtask to insert after'},
                            'insert_before': {'type': 'string', 'description': 'A subtask to insert before'},
                        },
                        'required': ['parent']
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Parent set successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "task",
                                "name": "Task Name",
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
                        'Circular reference',
                        value={
                            "errors": [
                                {
                                    "message": "parent: Cannot set a task as its own parent",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        'Circular hierarchy',
                        value={
                            "errors": [
                                {
                                    "message": "parent: Cannot create circular reference in task hierarchy",
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
                        'Task not found',
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
        summary="Set the parent of a task",
        description="Changes the parent of a task. A parent can be null for top-level tasks.",
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
        
        # Check if task exists
        try:
            task = Task.objects.get(gid=task_gid)
        except Task.DoesNotExist:
            return Response(
                not_found_error("task", task_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get request data
        data = request.data.get('data', request.data)
        
        # Validate parent field exists
        if 'parent' not in data:
            return Response(
                missing_field_error("parent"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parent_gid = data.get('parent')
        old_parent = task.parent
        
        # If parent is null, remove parent
        if parent_gid is None or parent_gid == 'null':
            task.parent = None
            task.save()
        else:
            # Validate parent GID format
            try:
                validate_uuid(parent_gid)
            except Exception:
                return Response(
                    invalid_gid_error("parent"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if parent task exists
            try:
                new_parent = Task.objects.get(gid=parent_gid)
            except Task.DoesNotExist:
                return Response(
                    not_found_error("parent", parent_gid),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prevent circular reference - task can't be its own parent
            if str(new_parent.gid) == str(task.gid):
                return Response(
                    bad_request_error("parent: Cannot set a task as its own parent"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check for indirect circular reference (A -> B -> C -> A)
            current = new_parent
            while current.parent:
                if str(current.parent.gid) == str(task.gid):
                    return Response(
                        bad_request_error("parent: Cannot create circular reference in task hierarchy"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                current = current.parent
            
            # Verify same workspace
            if new_parent.workspace.gid != task.workspace.gid:
                return Response(
                    bad_request_error("parent: Parent task must be in the same workspace"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            task.parent = new_parent
            task.save()
        
        # Update num_subtasks for old and new parents
        if old_parent:
            old_parent.num_subtasks = Task.objects.filter(parent=old_parent).count()
            old_parent.save()
        if task.parent:
            task.parent.num_subtasks = Task.objects.filter(parent=task.parent).count()
            task.parent.save()
        
        response_data = {
            'gid': str(task.gid),
            'resource_type': 'task',
            'name': task.name,
            'parent': {
                'gid': str(task.parent.gid),
                'resource_type': 'task',
                'name': task.parent.name
            } if task.parent else None,
            'workspace': {
                'gid': str(task.workspace.gid),
                'resource_type': 'workspace',
                'name': task.workspace.name
            }
        }
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)
