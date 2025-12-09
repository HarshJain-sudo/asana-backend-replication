from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from django.utils import timezone
from asana_projects.models.project import Project
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    invalid_field_error,
    bad_request_error,
    server_error
)


class UpdateProjectView(APIView):
    """
    Update a project.
    Matches Asana API: PUT /projects/{project_gid}
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to update',
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
                            'name': {'type': 'string'},
                            'notes': {'type': 'string'},
                            'color': {'type': 'string'},
                            'archived': {'type': 'boolean'},
                            'public': {'type': 'boolean'},
                            'due_on': {'type': 'string', 'format': 'date'},
                        }
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Project updated successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "project",
                                "name": "Updated Project"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Read-only field',
                        value={
                            "errors": [
                                {
                                    "message": "workspace: Cannot modify read-only field",
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
        summary="Update a project",
        description="Updates the project. Only the fields provided will be updated.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='PUT')
    def put(self, request, project_gid: str):
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
        
        # Get request data
        data = request.data.get('data', request.data)
        
        # Check for read-only fields
        read_only_fields = ['workspace', 'gid', 'resource_type', 'created_at']
        for field in read_only_fields:
            if field in data:
                return Response(
                    bad_request_error(f"{field}: Cannot modify read-only field"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Update allowed fields
        if 'name' in data:
            if not data['name'] or not isinstance(data['name'], str):
                return Response(
                    invalid_field_error("name", "Must be a non-empty string"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            project.name = data['name']
        
        if 'notes' in data:
            project.notes = data['notes']
        
        if 'html_notes' in data:
            project.html_notes = data['html_notes']
        
        if 'color' in data:
            color = data['color']
            valid_colors = [c[0] for c in Project.COLOR_CHOICES]
            if color and color not in valid_colors:
                return Response(
                    invalid_field_error("color", f"Invalid color. Must be one of: {', '.join(valid_colors)}"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            project.color = color
        
        if 'archived' in data:
            project.archived = bool(data['archived'])
        
        if 'public' in data:
            project.public = bool(data['public'])
        
        if 'completed' in data:
            project.completed = bool(data['completed'])
            if project.completed and not project.completed_at:
                project.completed_at = timezone.now()
        
        if 'due_on' in data:
            if data['due_on']:
                try:
                    from datetime import datetime
                    project.due_on = datetime.strptime(data['due_on'], '%Y-%m-%d').date()
                except ValueError:
                    return Response(
                        invalid_field_error("due_on", "Invalid date format. Use YYYY-MM-DD"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                project.due_on = None
        
        if 'start_on' in data:
            if data['start_on']:
                try:
                    from datetime import datetime
                    project.start_on = datetime.strptime(data['start_on'], '%Y-%m-%d').date()
                except ValueError:
                    return Response(
                        invalid_field_error("start_on", "Invalid date format. Use YYYY-MM-DD"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                project.start_on = None
        
        if 'default_view' in data:
            default_view = data['default_view']
            valid_views = [v[0] for v in Project.LAYOUT_CHOICES]
            if default_view not in valid_views:
                return Response(
                    invalid_field_error("default_view", f"Invalid view. Must be one of: {', '.join(valid_views)}"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            project.default_view = default_view
        
        # Save project
        try:
            project.save()
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'gid': str(project.gid),
            'resource_type': 'project',
            'name': project.name,
            'archived': project.archived,
            'color': project.color,
            'completed': project.completed,
            'completed_at': project.completed_at.isoformat() if project.completed_at else None,
            'default_view': project.default_view,
            'due_on': str(project.due_on) if project.due_on else None,
            'start_on': str(project.start_on) if project.start_on else None,
            'notes': project.notes,
            'public': project.public,
            'modified_at': project.modified_at.isoformat(),
            'workspace': {
                'gid': str(project.workspace.gid),
                'resource_type': 'workspace',
                'name': project.workspace.name
            }
        }
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)
