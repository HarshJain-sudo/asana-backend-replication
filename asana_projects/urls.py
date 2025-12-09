from django.urls import path
from asana_projects.views.get_project.get_project_view import GetProjectView
from asana_projects.views.get_projects.get_projects_view import GetProjectsView
from asana_projects.views.get_workspace_projects.get_workspace_projects_view import GetWorkspaceProjectsView
from asana_projects.views.create_project.create_project_view import CreateProjectView
from asana_projects.views.update_project.update_project_view import UpdateProjectView
from asana_projects.views.delete_project.delete_project_view import DeleteProjectView
from asana_projects.views.duplicate_project.duplicate_project_view import DuplicateProjectView
from asana_projects.views.get_project_tasks.get_project_tasks_view import GetProjectTasksView
from asana_projects.views.get_team_projects.get_team_projects_view import GetTeamProjectsView
from asana_projects.views.add_project_members.add_project_members_view import AddProjectMembersView
from asana_projects.views.remove_project_members.remove_project_members_view import RemoveProjectMembersView
from asana_projects.views.add_project_followers.add_project_followers_view import AddProjectFollowersView
from asana_projects.views.remove_project_followers.remove_project_followers_view import RemoveProjectFollowersView
from rest_framework.views import APIView
from rest_framework.response import Response


# Combined view for /projects/ endpoint (handles GET and POST)
class ProjectsListView(APIView):
    """Combined view for GET and POST on /projects/"""
    
    def get(self, request):
        return GetProjectsView().get(request)
    
    def post(self, request):
        return CreateProjectView().post(request)


# Combined view for /projects/{project_gid}/ endpoint (handles GET, PUT, DELETE)
class ProjectDetailView(APIView):
    """Combined view for GET, PUT, DELETE on /projects/{project_gid}/"""
    
    def get(self, request, project_gid):
        return GetProjectView().get(request, project_gid)
    
    def put(self, request, project_gid):
        return UpdateProjectView().put(request, project_gid)
    
    def delete(self, request, project_gid):
        return DeleteProjectView().delete(request, project_gid)


app_name = 'asana_projects'

urlpatterns = [
    # GET & POST /projects/ - List and Create projects
    path('projects/', ProjectsListView.as_view(), name='projects_list'),
    
    # GET, PUT, DELETE /projects/{project_gid}/ - Read, Update, Delete project
    path('projects/<str:project_gid>/', ProjectDetailView.as_view(), name='project_detail'),
    
    # POST /projects/{project_gid}/duplicate/ - Duplicate a project
    path('projects/<str:project_gid>/duplicate/', DuplicateProjectView.as_view(), name='duplicate_project'),
    
    # GET /projects/{project_gid}/tasks/ - Get tasks for a project
    path('projects/<str:project_gid>/tasks/', GetProjectTasksView.as_view(), name='get_project_tasks'),
    
    # POST /projects/{project_gid}/addMembers/ - Add members to a project
    path('projects/<str:project_gid>/addMembers/', AddProjectMembersView.as_view(), name='add_project_members'),
    
    # POST /projects/{project_gid}/removeMembers/ - Remove members from a project
    path('projects/<str:project_gid>/removeMembers/', RemoveProjectMembersView.as_view(), name='remove_project_members'),
    
    # POST /projects/{project_gid}/addFollowers/ - Add followers to a project
    path('projects/<str:project_gid>/addFollowers/', AddProjectFollowersView.as_view(), name='add_project_followers'),
    
    # POST /projects/{project_gid}/removeFollowers/ - Remove followers from a project
    path('projects/<str:project_gid>/removeFollowers/', RemoveProjectFollowersView.as_view(), name='remove_project_followers'),
    
    # GET /workspaces/{workspace_gid}/projects/ - Get projects in a workspace
    path('workspaces/<str:workspace_gid>/projects/', GetWorkspaceProjectsView.as_view(), name='get_workspace_projects'),
    
    # GET /teams/{team_gid}/projects/ - Get projects in a team
    path('teams/<str:team_gid>/projects/', GetTeamProjectsView.as_view(), name='get_team_projects'),
]
