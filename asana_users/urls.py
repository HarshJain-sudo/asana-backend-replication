"""
URL configuration for asana_users app.
"""
from django.urls import path
from asana_users.views.get_current_user.get_current_user_view import (
    GetCurrentUserView
)
from asana_users.views.get_user.get_user_view import (
    GetUserView
)
from asana_users.views.get_users.get_users_view import (
    GetUsersView
)
from asana_users.views.get_user_workspaces.get_user_workspaces_view import (
    GetUserWorkspacesView
)

app_name = 'asana_users'

urlpatterns = [
    path('users/me/', GetCurrentUserView.as_view(), name='get_current_user'),
    path('users/', GetUsersView.as_view(), name='get_users'),
    path('users/<str:user_gid>/', GetUserView.as_view(), name='get_user'),
    path(
        'users/<str:user_gid>/workspaces/',
        GetUserWorkspacesView.as_view(),
        name='get_user_workspaces'
    ),
]

