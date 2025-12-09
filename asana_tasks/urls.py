from django.urls import path
from asana_tasks.views.get_task.get_task_view import GetTaskView
from asana_tasks.views.get_tasks.get_tasks_view import GetTasksView
from asana_tasks.views.create_task.create_task_view import CreateTaskView
from asana_tasks.views.update_task.update_task_view import UpdateTaskView
from asana_tasks.views.delete_task.delete_task_view import DeleteTaskView
from asana_tasks.views.add_project_to_task.add_project_to_task_view import AddProjectToTaskView
from asana_tasks.views.remove_project_from_task.remove_project_from_task_view import RemoveProjectFromTaskView
from asana_tasks.views.add_tag_to_task.add_tag_to_task_view import AddTagToTaskView
from asana_tasks.views.remove_tag_from_task.remove_tag_from_task_view import RemoveTagFromTaskView
from asana_tasks.views.add_followers_to_task.add_followers_to_task_view import AddFollowersToTaskView
from asana_tasks.views.remove_followers_from_task.remove_followers_from_task_view import RemoveFollowersFromTaskView
from asana_tasks.views.get_subtasks.get_subtasks_view import GetSubtasksView
from asana_tasks.views.create_subtask.create_subtask_view import CreateSubtaskView
from asana_tasks.views.set_parent.set_parent_view import SetParentView
from asana_tasks.views.search_tasks.search_tasks_view import SearchTasksView
from asana_tasks.views.duplicate_task.duplicate_task_view import DuplicateTaskView
from asana_tasks.views.get_task_dependencies.get_task_dependencies_view import GetTaskDependenciesView
from asana_tasks.views.set_task_dependencies.set_task_dependencies_view import SetTaskDependenciesView
from asana_tasks.views.remove_task_dependencies.remove_task_dependencies_view import RemoveTaskDependenciesView
from asana_tasks.views.get_task_dependents.get_task_dependents_view import GetTaskDependentsView
from asana_tasks.views.set_task_dependents.set_task_dependents_view import SetTaskDependentsView
from asana_tasks.views.remove_task_dependents.remove_task_dependents_view import RemoveTaskDependentsView

app_name = 'asana_tasks'

urlpatterns = [
    # Basic CRUD operations
    path('tasks/', GetTasksView.as_view(), name='tasks'),
    path('tasks/<str:task_gid>/', GetTaskView.as_view(), name='task_detail'),
    
    # Subtasks (from /tasks/{task_gid}/subtasks in api_spec.txt)
    path('tasks/<str:task_gid>/subtasks/', GetSubtasksView.as_view(), name='get_subtasks'),
    path('tasks/<str:task_gid>/subtasks/', CreateSubtaskView.as_view(), name='create_subtask'),
    
    # Set Parent (from /tasks/{task_gid}/setParent in api_spec.txt)
    path('tasks/<str:task_gid>/setParent/', SetParentView.as_view(), name='set_parent'),
    
    # Relationship operations
    path('tasks/<str:task_gid>/addProject/', AddProjectToTaskView.as_view(), name='add_project_to_task'),
    path('tasks/<str:task_gid>/removeProject/', RemoveProjectFromTaskView.as_view(), name='remove_project_from_task'),
    path('tasks/<str:task_gid>/addTag/', AddTagToTaskView.as_view(), name='add_tag_to_task'),
    path('tasks/<str:task_gid>/removeTag/', RemoveTagFromTaskView.as_view(), name='remove_tag_from_task'),
    path('tasks/<str:task_gid>/addFollowers/', AddFollowersToTaskView.as_view(), name='add_followers_to_task'),
    path('tasks/<str:task_gid>/removeFollowers/', RemoveFollowersFromTaskView.as_view(), name='remove_followers_from_task'),
    
    # Duplicate task
    path('tasks/<str:task_gid>/duplicate/', DuplicateTaskView.as_view(), name='duplicate_task'),
    
    # Dependencies
    path('tasks/<str:task_gid>/dependencies/', GetTaskDependenciesView.as_view(), name='get_task_dependencies'),
    path('tasks/<str:task_gid>/dependencies/', SetTaskDependenciesView.as_view(), name='set_task_dependencies'),
    path('tasks/<str:task_gid>/dependencies/remove/', RemoveTaskDependenciesView.as_view(), name='remove_task_dependencies'),
    
    # Dependents
    path('tasks/<str:task_gid>/dependents/', GetTaskDependentsView.as_view(), name='get_task_dependents'),
    path('tasks/<str:task_gid>/dependents/', SetTaskDependentsView.as_view(), name='set_task_dependents'),
    path('tasks/<str:task_gid>/dependents/remove/', RemoveTaskDependentsView.as_view(), name='remove_task_dependents'),
    
    # Search tasks (from /workspaces/{workspace_gid}/tasks/search in api_spec.txt)
    path('workspaces/<str:workspace_gid>/tasks/search/', SearchTasksView.as_view(), name='search_tasks'),
]

