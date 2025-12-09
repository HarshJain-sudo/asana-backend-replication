from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project, ProjectMember
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    missing_field_error,
    server_error
)


class RemoveProjectMembersView(APIView):
    """
    Remove users from a project.
    Matches Asana API: POST /projects/{project_gid}/removeMembers
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to remove members from',
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
                            'members': {
                                'type': 'string',
                                'description': 'Comma-separated list of user GIDs to remove'
                            }
                        },
                        'required': ['members']
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Members removed successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "project",
                                "name": "Project Name"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid request",
                examples=[
                    OpenApiExample(
                        'Missing members',
                        value={
                            "errors": [
                                {
                                    "message": "members: Missing input",
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
        summary="Remove users from a project",
        description="Removes users from a project.",
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
            project = Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return Response(
                not_found_error("project", project_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get request data
        data = request.data.get('data', request.data)
        
        # Validate members field
        members = data.get('members')
        if not members:
            return Response(
                missing_field_error("members"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse members (can be comma-separated string or list)
        if isinstance(members, str):
            member_gids = [m.strip() for m in members.split(',')]
        else:
            member_gids = members
        
        # Remove each member
        try:
            for user_gid in member_gids:
                validate_uuid(user_gid)
                ProjectMember.objects.filter(project=project, user__gid=user_gid).delete()
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response_data = {
            'gid': str(project.gid),
            'resource_type': 'project',
            'name': project.name
        }
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)
