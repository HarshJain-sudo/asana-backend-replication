"""
URL configuration for asana_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import FileResponse, JsonResponse
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
import os


def api_spec_view(request):
    """Serve the Asana API specification file."""
    spec_path = os.path.join(settings.BASE_DIR, 'api_spec.txt')
    
    if os.path.exists(spec_path):
        # Check if user wants JSON format
        if request.GET.get('format') == 'json':
            with open(spec_path, 'r') as f:
                content = f.read()
            return JsonResponse({
                'data': {
                    'name': 'Asana API Specification',
                    'version': '1.0',
                    'format': 'OpenAPI 3.0',
                    'content': content[:10000] + '...' if len(content) > 10000 else content
                }
            })
        
        # Return as file download
        return FileResponse(
            open(spec_path, 'rb'),
            as_attachment=True,
            filename='api_spec.txt',
            content_type='text/plain'
        )
    else:
        return JsonResponse({
            'errors': [{
                'message': 'api_spec.txt not found',
                'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors'
            }]
        }, status=404)


def api_info_view(request):
    """Return API information and available endpoints."""
    return JsonResponse({
        'data': {
            'name': 'Asana API Clone',
            'version': '1.0',
            'base_url': '/api/1.0/',
            'documentation': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/',
                'openapi_schema': '/api/schema/',
                'original_spec': '/api/spec/'
            },
            'endpoints': {
                'workspaces': {
                    'list': 'GET /api/1.0/workspaces/',
                    'detail': 'GET /api/1.0/workspaces/{workspace_gid}/',
                },
                'projects': {
                    'list': 'GET /api/1.0/projects/',
                    'create': 'POST /api/1.0/projects/',
                    'detail': 'GET /api/1.0/projects/{project_gid}/',
                    'update': 'PUT /api/1.0/projects/{project_gid}/',
                    'delete': 'DELETE /api/1.0/projects/{project_gid}/',
                    'duplicate': 'POST /api/1.0/projects/{project_gid}/duplicate/',
                    'tasks': 'GET /api/1.0/projects/{project_gid}/tasks/',
                    'add_members': 'POST /api/1.0/projects/{project_gid}/addMembers/',
                    'remove_members': 'POST /api/1.0/projects/{project_gid}/removeMembers/',
                    'add_followers': 'POST /api/1.0/projects/{project_gid}/addFollowers/',
                    'remove_followers': 'POST /api/1.0/projects/{project_gid}/removeFollowers/',
                    'workspace_projects': 'GET /api/1.0/workspaces/{workspace_gid}/projects/',
                    'team_projects': 'GET /api/1.0/teams/{team_gid}/projects/',
                },
                'tasks': {
                    'list': 'GET /api/1.0/tasks/',
                    'create': 'POST /api/1.0/tasks/',
                    'detail': 'GET /api/1.0/tasks/{task_gid}/',
                    'update': 'PUT /api/1.0/tasks/{task_gid}/',
                    'delete': 'DELETE /api/1.0/tasks/{task_gid}/',
                    'subtasks': 'GET /api/1.0/tasks/{task_gid}/subtasks/',
                    'create_subtask': 'POST /api/1.0/tasks/{task_gid}/subtasks/',
                    'set_parent': 'POST /api/1.0/tasks/{task_gid}/setParent/',
                    'search': 'GET /api/1.0/workspaces/{workspace_gid}/tasks/search/',
                },
                'users': {
                    'list': 'GET /api/1.0/users/',
                    'detail': 'GET /api/1.0/users/{user_gid}/',
                },
                'teams': {
                    'list': 'GET /api/1.0/teams/',
                    'detail': 'GET /api/1.0/teams/{team_gid}/',
                },
                'tags': {
                    'list': 'GET /api/1.0/tags/',
                    'detail': 'GET /api/1.0/tags/{tag_gid}/',
                }
            }
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Spec and Info
    path('api/spec/', api_spec_view, name='api-spec'),
    path('api/info/', api_info_view, name='api-info'),
    
    # Asana API Endpoints (matching Asana API spec format)
    path('api/1.0/', include('asana_workspaces.urls')),
    path('api/1.0/', include('asana_users.urls')),
    path('api/1.0/', include('asana_projects.urls')),
    path('api/1.0/', include('asana_teams.urls')),
    path('api/1.0/', include('asana_tags.urls')),
    path('api/1.0/', include('asana_tasks.urls')),
    path('api/1.0/', include('asana_stories.urls')),
    path('api/1.0/', include('asana_attachments.urls')),
    path('api/1.0/', include('asana_webhooks.urls')),
]
