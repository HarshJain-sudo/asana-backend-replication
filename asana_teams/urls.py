from django.urls import path
from asana_teams.views.get_team.get_team_view import (
    GetTeamView
)
from asana_teams.views.get_teams.get_teams_view import (
    GetTeamsView
)
from asana_teams.views.get_workspace_teams.get_workspace_teams_view import (
    GetWorkspaceTeamsView
)
from asana_teams.views.create_team.create_team_view import (
    CreateTeamView
)
from asana_teams.views.add_user_to_team.add_user_to_team_view import (
    AddUserToTeamView
)
from asana_teams.views.remove_user_from_team.remove_user_from_team_view import (
    RemoveUserFromTeamView
)
from asana_teams.views.get_teams_for_user.get_teams_for_user_view import (
    GetTeamsForUserView
)

app_name = 'asana_teams'

urlpatterns = [
    # Teams CRUD
    path('teams/', GetTeamsView.as_view(), name='get_teams'),  # GET list
    path('teams/', CreateTeamView.as_view(), name='create_team'),  # POST create
    path('teams/<str:team_gid>/', GetTeamView.as_view(), name='get_team'),  # GET single, PUT update
    
    # Team relationships
    path('teams/<str:team_gid>/addUser', AddUserToTeamView.as_view(), name='add_user_to_team'),
    path('teams/<str:team_gid>/removeUser', RemoveUserFromTeamView.as_view(), name='remove_user_from_team'),
    
    # Workspace teams
    path(
        'workspaces/<str:workspace_gid>/teams/',
        GetWorkspaceTeamsView.as_view(),
        name='get_workspace_teams'
    ),
    
    # User teams
    path('users/<str:user_gid>/teams', GetTeamsForUserView.as_view(), name='get_teams_for_user'),
]

