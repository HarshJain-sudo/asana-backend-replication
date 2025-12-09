from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project, ProjectFollower
from asana_workspaces.models.workspace import Workspace
from asana_teams.models.team import Team
from asana_users.models.user import User
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    missing_field_error,
    invalid_field_error,
    server_error
)
from datetime import datetime


class CreateProjectView(APIView):
    """
    Create a project.
    Matches Asana API: POST /projects
    """
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'workspace': {'type': 'string'},
                            'team': {'type': 'string'},
                            'notes': {'type': 'string'},
                            'html_notes': {'type': 'string'},
                            'color': {'type': 'string'},
                            'default_view': {'type': 'string'},
                            'public': {'type': 'boolean'},
                            'due_on': {'type': 'string'},
                            'due_date': {'type': 'string'},
                            'start_on': {'type': 'string'},
                            'owner': {'type': 'string'},
                            'followers': {'type': 'string'},
                        },
                        'required': ['name', 'workspace']
                    }
                }
            }
        },
        responses={
            201: OpenApiResponse(description="Project created successfully"),
            400: OpenApiResponse(description="Invalid request"),
        },
        summary="Create a project",
        description="Creates a new project in a workspace or team.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request):
        # Get request data
        data = request.data.get('data', request.data)
        
        # Validate required fields
        name = data.get('name')
        if not name:
            return Response(
                missing_field_error("name"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        workspace_gid = data.get('workspace')
        if not workspace_gid:
            return Response(
                missing_field_error("workspace"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate workspace
        try:
            validate_uuid(workspace_gid)
            workspace = Workspace.objects.get(gid=workspace_gid)
        except Exception:
            return Response(
                not_found_error("workspace", workspace_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate team if provided
        team = None
        team_gid = data.get('team')
        if team_gid:
            try:
                validate_uuid(team_gid)
                team = Team.objects.get(gid=team_gid)
                if team.workspace.gid != workspace.gid:
                    return Response(
                        invalid_field_error("team", "Team must belong to the specified workspace"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Team.DoesNotExist:
                return Response(
                    not_found_error("team", team_gid),
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Validate owner if provided
        owner = None
        owner_gid = data.get('owner')
        if owner_gid:
            try:
                validate_uuid(owner_gid)
                owner = User.objects.get(gid=owner_gid)
            except User.DoesNotExist:
                return Response(
                    not_found_error("owner", owner_gid),
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Validate color if provided
        color = data.get('color')
        valid_colors = [c[0] for c in Project.COLOR_CHOICES]
        if color and color not in valid_colors:
            return Response(
                invalid_field_error("color", f"Invalid color. Must be one of: {', '.join(valid_colors)}"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate default_view if provided
        default_view = data.get('default_view', 'list')
        valid_views = [v[0] for v in Project.LAYOUT_CHOICES]
        if default_view not in valid_views:
            return Response(
                invalid_field_error("default_view", f"Invalid view. Must be one of: {', '.join(valid_views)}"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse dates
        due_on = data.get('due_on') or data.get('due_date')
        start_on = data.get('start_on')
        
        due_on_date = None
        start_on_date = None
        
        if due_on:
            try:
                due_on_date = datetime.strptime(due_on, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    invalid_field_error("due_on", "Invalid date format. Use YYYY-MM-DD"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if start_on:
            try:
                start_on_date = datetime.strptime(start_on, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    invalid_field_error("start_on", "Invalid date format. Use YYYY-MM-DD"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create project
        try:
            project = Project.objects.create(
                name=name,
                workspace=workspace,
                team=team,
                owner=owner,
                notes=data.get('notes', ''),
                html_notes=data.get('html_notes', ''),
                color=color,
                default_view=default_view,
                public=data.get('public', False),
                archived=data.get('archived', False),
                due_on=due_on_date,
                start_on=start_on_date,
            )
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Add followers if provided
        followers_list = []
        followers_str = data.get('followers')
        if followers_str:
            follower_gids = [f.strip() for f in followers_str.split(',') if f.strip()]
            for follower_gid in follower_gids:
                try:
                    validate_uuid(follower_gid)
                    user = User.objects.get(gid=follower_gid)
                    ProjectFollower.objects.get_or_create(project=project, user=user)
                    followers_list.append({
                        'gid': str(user.gid),
                        'resource_type': 'user',
                        'name': user.name
                    })
                except User.DoesNotExist:
                    pass  # Skip invalid followers
        
        # Build full response matching Asana API spec
        response_data = {
            'gid': str(project.gid),
            'resource_type': 'project',
            'name': project.name,
            'archived': project.archived,
            'color': project.color,
            'created_at': project.created_at.isoformat(),
            'current_status': data.get('current_status'),  # Pass through if provided
            'current_status_update': data.get('current_status_update'),
            'custom_field_settings': [],
            'default_view': project.default_view,
            'due_date': str(project.due_on) if project.due_on else None,
            'due_on': str(project.due_on) if project.due_on else None,
            'html_notes': project.html_notes or (f'<body>{project.notes}</body>' if project.notes else ''),
            'members': [],
            'modified_at': project.modified_at.isoformat(),
            'notes': project.notes,
            'public': project.public,
            'privacy_setting': 'public_to_workspace' if project.public else 'private',
            'start_on': str(project.start_on) if project.start_on else None,
            'default_access_level': data.get('default_access_level', 'editor'),
            'minimum_access_level_for_customization': data.get('minimum_access_level_for_customization', 'editor'),
            'minimum_access_level_for_sharing': data.get('minimum_access_level_for_sharing', 'editor'),
            'custom_fields': [],
            'completed': project.completed,
            'completed_at': project.completed_at.isoformat() if project.completed_at else None,
            'completed_by': None,
            'followers': followers_list,
            'owner': {
                'gid': str(owner.gid),
                'resource_type': 'user',
                'name': owner.name
            } if owner else None,
            'team': {
                'gid': str(team.gid),
                'resource_type': 'team',
                'name': team.name
            } if team else None,
            'icon': project.icon,
            'permalink_url': f'https://app.asana.com/0/{project.gid}',
            'project_brief': None,
            'created_from_template': None,
            'workspace': {
                'gid': str(workspace.gid),
                'resource_type': 'workspace',
                'name': workspace.name
            }
        }
        
        return Response({'data': response_data}, status=status.HTTP_201_CREATED)
