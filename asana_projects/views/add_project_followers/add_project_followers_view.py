from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project, ProjectFollower
from asana_users.models.user import User
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    missing_field_error,
    server_error
)


class AddProjectFollowersView(APIView):
    """
    Add followers to a project.
    Matches Asana API: POST /projects/{project_gid}/addFollowers
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to add followers to',
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
                            'followers': {
                                'type': 'string',
                                'description': 'Comma-separated list of user GIDs to add as followers'
                            }
                        },
                        'required': ['followers']
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Followers added successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "project",
                                "name": "Project Name",
                                "followers": [
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
                        'Missing followers',
                        value={
                            "errors": [
                                {
                                    "message": "followers: Missing input",
                                    "help": "For more information..."
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Project or user not found"
            ),
        },
        summary="Add followers to a project",
        description="Adds users to a project as followers.",
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
        
        # Validate followers field
        followers = data.get('followers')
        if not followers:
            return Response(
                missing_field_error("followers"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse followers (can be comma-separated string or list)
        if isinstance(followers, str):
            follower_gids = [f.strip() for f in followers.split(',')]
        else:
            follower_gids = followers
        
        # Add each follower
        added_followers = []
        for user_gid in follower_gids:
            try:
                validate_uuid(user_gid)
                user = User.objects.get(gid=user_gid)
                
                # Create follower if doesn't exist
                follower, created = ProjectFollower.objects.get_or_create(
                    project=project,
                    user=user
                )
                
                added_followers.append({
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
            'followers': added_followers
        }
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)
