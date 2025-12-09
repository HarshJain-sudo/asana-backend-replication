from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project
from asana_teams.models.team import Team
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    invalid_field_error
)


class GetTeamProjectsView(APIView):
    """
    Get projects in a team.
    Returns projects in the specified team.
    Matches Asana API: GET /teams/{team_gid}/projects
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='team_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The team to get projects from',
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
                name='archived',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Only return archived projects',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully retrieved projects",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "project",
                                    "name": "Project 1"
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Team not found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "team: Unknown object: 12345",
                                    "help": "For more information..."
                                }
                            ]
                        }
                    )
                ]
            ),
        },
        summary="Get projects in a team",
        description="Returns the projects in the specified team.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, team_gid: str):
        # Validate team GID format
        try:
            validate_uuid(team_gid)
        except Exception:
            return Response(
                invalid_gid_error("team_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if team exists
        try:
            team = Team.objects.get(gid=team_gid)
        except Team.DoesNotExist:
            return Response(
                not_found_error("team", team_gid),
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
        
        # Build query
        queryset = Project.objects.filter(team=team)
        
        # Filter by archived
        archived = request.query_params.get('archived')
        if archived is not None:
            archived_bool = archived.lower() == 'true'
            queryset = queryset.filter(archived=archived_bool)
        
        # Apply pagination
        projects = queryset[offset:offset + limit]
        
        projects_list = [
            {
                'gid': str(project.gid),
                'resource_type': 'project',
                'name': project.name,
                'archived': project.archived,
                'color': project.color,
            }
            for project in projects
        ]
        
        return Response({'data': projects_list}, status=status.HTTP_200_OK)
