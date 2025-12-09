from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project, ProjectFollower
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    missing_field_error,
    server_error
)


class RemoveProjectFollowersView(APIView):
    """
    Remove followers from a project.
    Matches Asana API: POST /projects/{project_gid}/removeFollowers
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to remove followers from',
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
                                'description': 'Comma-separated list of user GIDs to remove'
                            }
                        },
                        'required': ['followers']
                    }
                }
            }
        },
        responses={
            200: OpenApiResponse(
                description="Followers removed successfully",
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
                description="Invalid request"
            ),
            404: OpenApiResponse(
                description="Project not found"
            ),
        },
        summary="Remove followers from a project",
        description="Removes users from a project as followers.",
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
        
        # Remove each follower
        try:
            for user_gid in follower_gids:
                validate_uuid(user_gid)
                ProjectFollower.objects.filter(project=project, user__gid=user_gid).delete()
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
