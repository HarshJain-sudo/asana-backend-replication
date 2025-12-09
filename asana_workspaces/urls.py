"""
URL configuration for asana_workspaces app.
"""
from django.urls import path
from asana_workspaces.views.get_workspace.get_workspace_view import (
    GetWorkspaceView
)
from asana_workspaces.views.get_workspaces.get_workspaces_view import (
    GetWorkspacesView
)
from asana_workspaces.views.add_user_to_workspace.add_user_to_workspace_view import (
    AddUserToWorkspaceView
)
from asana_workspaces.views.remove_user_from_workspace.remove_user_from_workspace_view import (
    RemoveUserFromWorkspaceView
)
from asana_workspaces.views.get_workspace_events.get_workspace_events_view import (
    GetWorkspaceEventsView
)

app_name = 'asana_workspaces'

urlpatterns = [
    # Workspaces CRUD
    path('workspaces/', GetWorkspacesView.as_view(), name='get_workspaces'),  # GET list, POST create
    path('workspaces/<str:workspace_gid>/', GetWorkspaceView.as_view(), name='get_workspace'),  # GET single, PUT update, DELETE
    
    # Workspace relationships
    path('workspaces/<str:workspace_gid>/addUser', AddUserToWorkspaceView.as_view(), name='add_user_to_workspace'),
    path('workspaces/<str:workspace_gid>/removeUser', RemoveUserFromWorkspaceView.as_view(), name='remove_user_from_workspace'),
    path('workspaces/<str:workspace_gid>/events', GetWorkspaceEventsView.as_view(), name='get_workspace_events'),
]

