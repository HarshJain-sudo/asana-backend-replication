from django.urls import path
from asana_stories.views.get_story.get_story_view import (
    GetStoryView
)
from asana_stories.views.get_task_stories.get_task_stories_view import (
    GetTaskStoriesView
)

app_name = 'asana_stories'

urlpatterns = [
    path('stories/<str:story_gid>/', GetStoryView.as_view(), name='get_story'),
    path(
        'tasks/<str:task_gid>/stories/',
        GetTaskStoriesView.as_view(),
        name='get_task_stories'
    ),
]

