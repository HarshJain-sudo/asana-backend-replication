from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
import uuid
from asana_projects.models.project import Project
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    missing_field_error,
    server_error
)


class DuplicateProjectView(APIView):
    """
    Duplicate a project.
    Creates and returns a job that will asynchronously handle the duplication.
    Matches Asana API: POST /projects/{project_gid}/duplicate
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to duplicate',
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
                            'name': {'type': 'string', 'description': 'Name of the new project'},
                            'include': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Elements to duplicate (members, notes, task_notes, etc.)'
                            },
                        },
                        'required': ['name']
                    }
                }
            }
        },
        responses={
            201: OpenApiResponse(
                description="Job created to handle duplication",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "job-12345",
                                "resource_type": "job",
                                "resource_subtype": "duplicate_project",
                                "status": "in_progress",
                                "new_project": {
                                    "gid": "new-project-gid",
                                    "resource_type": "project",
                                    "name": "Duplicated Project"
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
                        'Missing name',
                        value={
                            "errors": [
                                {
                                    "message": "name: Missing input",
                                    "help": "For more information..."
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
        summary="Duplicate a project",
        description="Creates a copy of an existing project with a new name.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request, project_gid: str):
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
            original_project = Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return Response(
                not_found_error("project", project_gid),
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
        
        # Get include options
        include = data.get('include', [])
        
        # Create duplicated project (synchronously for simplicity)
        try:
            new_project = Project.objects.create(
                name=name,
                workspace=original_project.workspace,
                team=original_project.team,
                notes=original_project.notes if 'notes' in include or 'task_notes' in include else '',
                html_notes=original_project.html_notes if 'notes' in include else '',
                color=original_project.color,
                default_view=original_project.default_view,
                public=original_project.public,
                archived=False,
            )
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return job response (in a real implementation, this would be async)
        job_gid = str(uuid.uuid4())
        
        response_data = {
            'gid': job_gid,
            'resource_type': 'job',
            'resource_subtype': 'duplicate_project',
            'status': 'succeeded',  # Synchronous, so already done
            'new_project': {
                'gid': str(new_project.gid),
                'resource_type': 'project',
                'name': new_project.name
            }
        }
        
        return Response({'data': response_data}, status=status.HTTP_201_CREATED)
