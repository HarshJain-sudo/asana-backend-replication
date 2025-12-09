from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from django.db.models import Q
from asana_tasks.models.task import Task
from asana_workspaces.models.workspace import Workspace
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    invalid_field_error
)


class SearchTasksView(APIView):
    """
    Search tasks in a workspace.
    Performs advanced search on tasks with multiple filter options.
    Matches Asana API: GET /workspaces/{workspace_gid}/tasks/search
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The workspace to search in',
                required=True
            ),
            OpenApiParameter(
                name='text',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Full-text search on task name and description',
                required=False
            ),
            OpenApiParameter(
                name='resource_subtype',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by resource_subtype (default_task, milestone, approval)',
                required=False
            ),
            OpenApiParameter(
                name='completed',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Filter by completion status',
                required=False
            ),
            OpenApiParameter(
                name='is_subtask',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Filter for subtasks only',
                required=False
            ),
            OpenApiParameter(
                name='due_on.before',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Due date before (ISO 8601 date)',
                required=False
            ),
            OpenApiParameter(
                name='due_on.after',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Due date after (ISO 8601 date)',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Search results",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "task",
                                    "name": "Bug fix"
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
                        'Invalid date format',
                        value={
                            "errors": [
                                {
                                    "message": "due_on.before: Invalid date format. Use YYYY-MM-DD",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Workspace not found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "workspace: Unknown object: 12345",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
                                }
                            ]
                        }
                    )
                ]
            ),
        },
        summary="Search tasks in a workspace",
        description="Performs full-text search on both task name and description with advanced filtering.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, workspace_gid: str):
        # Validate workspace GID format
        try:
            validate_uuid(workspace_gid)
        except Exception:
            return Response(
                invalid_gid_error("workspace_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if workspace exists
        try:
            workspace = Workspace.objects.get(gid=workspace_gid)
        except Workspace.DoesNotExist:
            return Response(
                not_found_error("workspace", workspace_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Build query
        queryset = Task.objects.filter(workspace=workspace)
        
        # Text search (full-text on name and notes)
        text = request.query_params.get('text')
        if text:
            queryset = queryset.filter(
                Q(name__icontains=text) | Q(notes__icontains=text)
            )
        
        # Resource subtype filter
        resource_subtype = request.query_params.get('resource_subtype')
        if resource_subtype:
            valid_subtypes = ['default_task', 'milestone', 'approval']
            if resource_subtype not in valid_subtypes:
                return Response(
                    invalid_field_error(
                        "resource_subtype", 
                        f"Invalid value. Must be one of: {', '.join(valid_subtypes)}"
                    ),
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(resource_subtype=resource_subtype)
        
        # Completed filter
        completed = request.query_params.get('completed')
        if completed is not None:
            completed_bool = completed.lower() == 'true'
            queryset = queryset.filter(completed=completed_bool)
        
        # Subtask filter
        is_subtask = request.query_params.get('is_subtask')
        if is_subtask is not None:
            is_subtask_bool = is_subtask.lower() == 'true'
            if is_subtask_bool:
                queryset = queryset.filter(parent__isnull=False)
            else:
                queryset = queryset.filter(parent__isnull=True)
        
        # Due date filters
        due_on_before = request.query_params.get('due_on.before')
        if due_on_before:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(due_on_before, '%Y-%m-%d').date()
                queryset = queryset.filter(due_on__lt=date_obj)
            except ValueError:
                return Response(
                    invalid_field_error("due_on.before", "Invalid date format. Use YYYY-MM-DD"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        due_on_after = request.query_params.get('due_on.after')
        if due_on_after:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(due_on_after, '%Y-%m-%d').date()
                queryset = queryset.filter(due_on__gt=date_obj)
            except ValueError:
                return Response(
                    invalid_field_error("due_on.after", "Invalid date format. Use YYYY-MM-DD"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Limit results
        queryset = queryset[:100]
        
        tasks_list = [
            {
                'gid': str(task.gid),
                'resource_type': 'task',
                'name': task.name,
                'resource_subtype': task.resource_subtype,
                'completed': task.completed,
            }
            for task in queryset
        ]
        
        return Response({'data': tasks_list}, status=status.HTTP_200_OK)
