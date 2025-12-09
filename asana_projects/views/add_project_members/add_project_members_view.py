from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project, ProjectMember
from asana_users.models.user import User
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    missing_field_error,
    server_error
)


class AddProjectMembersView(APIView):
    """
    Add users to a project.
    Matches Asana API: POST /projects/{project_gid}/addMembers
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to add members to',
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
                                'description': 'Comma-separated list of user GIDs to add'
                            }
                        },
                        'required': ['members']
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Members added successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "project",
                                "name": "Project Name",
                                "members": [
                                    {"gid": "user-1", "resource_type": "user", "name": "User 1"}
                                ]
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
                description="Project or user not found",
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
        summary="Add users to a project",
        description="Adds users to a project as members.",
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
        
        # Add each member
        added_members = []
        for user_gid in member_gids:
            try:
                validate_uuid(user_gid)
                user = User.objects.get(gid=user_gid)
                
                # Create membership if doesn't exist
                membership, created = ProjectMember.objects.get_or_create(
                    project=project,
                    user=user,
                    defaults={'access_level': 'editor'}
                )
                
                added_members.append({
                    'gid': str(user.gid),
                    'resource_type': 'user',
                    'name': user.name
                })
            except User.DoesNotExist:
                return Response(
                    not_found_error("user", user_gid),
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    server_error(str(e)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        response_data = {
            'gid': str(project.gid),
            'resource_type': 'project',
            'name': project.name,
            'members': added_members
        }
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)
