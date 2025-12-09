from django.urls import path
from asana_tags.views.get_tag.get_tag_view import (
    GetTagView
)
from asana_tags.views.get_tags.get_tags_view import (
    GetTagsView
)
from asana_tags.views.get_workspace_tags.get_workspace_tags_view import (
    GetWorkspaceTagsView
)
from asana_tags.views.create_tag.create_tag_view import (
    CreateTagView
)
from asana_tags.views.create_tag_in_workspace.create_tag_in_workspace_view import (
    CreateTagInWorkspaceView
)
from asana_tags.views.get_task_tags.get_task_tags_view import (
    GetTaskTagsView
)

app_name = 'asana_tags'

urlpatterns = [
    # Tags CRUD
    path('tags/', GetTagsView.as_view(), name='get_tags'),  # GET list
    path('tags/', CreateTagView.as_view(), name='create_tag'),  # POST create
    path('tags/<str:tag_gid>/', GetTagView.as_view(), name='get_tag'),  # GET single, PUT update, DELETE
    
    # Workspace tags
    path(
        'workspaces/<str:workspace_gid>/tags/',
        GetWorkspaceTagsView.as_view(),
        name='get_workspace_tags'
    ),  # GET list
    path(
        'workspaces/<str:workspace_gid>/tags/',
        CreateTagInWorkspaceView.as_view(),
        name='create_tag_in_workspace'
    ),  # POST create
    
    # Task tags
    path(
        'tasks/<str:task_gid>/tags/',
        GetTaskTagsView.as_view(),
        name='get_task_tags'
    ),  # GET list
]

