from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project
from asana_tasks.models.task import Task
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    invalid_field_error
)


class GetProjectTasksView(APIView):
    """
    Get tasks for a project.
    Returns tasks in the project.
    Matches Asana API: GET /projects/{project_gid}/tasks
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to get tasks from',
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
                type=int,
                location=OpenApiParameter.QUERY,
                description='Offset for pagination',
                required=False
            ),
            OpenApiParameter(
                name='completed_since',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Only return tasks completed since this time',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved tasks",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "task",
                                    "name": "Task 1"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Project not found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "project: Unknown object: 12345",
                                    "help": "For more information..."
                                }
                            ]
                        }
                    )
                ]
            ),
        },
        summary="Get tasks from a project",
        description="Returns the compact task records for all tasks within the given project.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, project_gid: str):
        # Validate project GID format
        try:
            validate_uuid(project_gid)
        except Exception:
            return Response(
                invalid_gid_error("project_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if project exists
        try:
            project = Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return Response(
                not_found_error("project", project_gid),
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
        
        try:
            offset = int(request.query_params.get('offset', 0))
            if offset < 0:
                return Response(
                    invalid_field_error("offset", "Must be >= 0"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                invalid_field_error("offset", "Must be a valid integer"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get tasks for this project (using TaskProject relation)
        from asana_tasks.models.task_project import TaskProject
        task_projects = TaskProject.objects.filter(project=project).select_related('task')
        tasks = [tp.task for tp in task_projects[offset:offset + limit]]
        
        tasks_list = [
            {
                'gid': str(task.gid),
                'resource_type': 'task',
                'name': task.name,
                'resource_subtype': task.resource_subtype,
                'completed': task.completed,
            }
            for task in tasks
        ]
        
        return Response({'data': tasks_list}, status=status.HTTP_200_OK)
