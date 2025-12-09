# Code Generation Summary

Generated: 2025-12-10 01:23:44
Mode: DRY RUN

## Statistics

- **Total APIs Generated**: 191
- **Errors**: 0

## Generated APIs

### POST /projects

**Operation**: createProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/create_project_view/create_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/create_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### PUT /projects/{project_gid}

**Operation**: updateProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/update_project_view/update_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/update_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### POST /teams/{team_gid}/projects

**Operation**: createProjectForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/create_project_for_team_view/create_project_for_team_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/create_project_for_team_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### POST /workspaces/{workspace_gid}/projects

**Operation**: createProjectForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/create_project_for_workspace_view/create_project_for_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/create_project_for_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### PUT /tasks/{task_gid}

**Operation**: updateTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/update_task_view/update_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/update_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### POST /teams

**Operation**: createTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/create_team_view/create_team_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/interactors/create_team_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### PUT /teams/{team_gid}

**Operation**: updateTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/update_team_view/update_team_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/interactors/update_team_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### PUT /users/{user_gid}

**Operation**: updateUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/update_user_view/update_user_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_users/interactors/update_user_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### PUT /workspaces/{workspace_gid}/users/{user_gid}

**Operation**: updateUserForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/update_user_for_workspace_view/update_user_for_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_users/interactors/update_user_for_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### PUT /workspaces/{workspace_gid}

**Operation**: updateWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/update_workspace_view/update_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/interactors/update_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### GET /projects

**Operation**: getProjects

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/get_projects_view/get_projects_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### GET /projects/{project_gid}

**Operation**: getProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/get_project_view/get_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### DELETE /projects/{project_gid}

**Operation**: deleteProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/delete_project_view/delete_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/delete_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### GET /tasks/{task_gid}/projects

**Operation**: getProjectsForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/get_projects_for_task_view/get_projects_for_task_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### GET /projects/{project_gid}/task_counts

**Operation**: getTaskCountsForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/get_task_counts_for_project_view/get_task_counts_for_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### DELETE /tasks/{task_gid}

**Operation**: deleteTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/delete_task_view/delete_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/delete_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### GET /sections/{section_gid}/tasks

**Operation**: getTasksForSection

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/get_tasks_for_section_view/get_tasks_for_section_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### GET /tags/{tag_gid}/tasks

**Operation**: getTasksForTag

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/get_tasks_for_tag_view/get_tasks_for_tag_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### GET /user_task_lists/{user_task_list_gid}/tasks

**Operation**: getTasksForUserTaskList

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/get_tasks_for_user_task_list_view/get_tasks_for_user_task_list_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id}

**Operation**: getTaskForCustomID

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/get_task_for_custom_id_view/get_task_for_custom_id_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### GET /teams/{team_gid}

**Operation**: getTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/get_team_view/get_team_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### GET /workspaces/{workspace_gid}/teams

**Operation**: getTeamsForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/get_teams_for_workspace_view/get_teams_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### GET /users/{user_gid}/teams

**Operation**: getTeamsForUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/get_teams_for_user_view/get_teams_for_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### GET /users

**Operation**: getUsers

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_users_view/get_users_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /users/{user_gid}

**Operation**: getUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_user_view/get_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /users/{user_gid}/favorites

**Operation**: getFavoritesForUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_favorites_for_user_view/get_favorites_for_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /teams/{team_gid}/users

**Operation**: getUsersForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_users_for_team_view/get_users_for_team_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /workspaces/{workspace_gid}/users

**Operation**: getUsersForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_users_for_workspace_view/get_users_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /workspaces/{workspace_gid}/users/{user_gid}

**Operation**: getUserForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_users/views/get_user_for_workspace_view/get_user_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_users/serializers.py`

### GET /workspaces

**Operation**: getWorkspaces

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/get_workspaces_view/get_workspaces_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### GET /workspaces/{workspace_gid}

**Operation**: getWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/get_workspace_view/get_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### GET /workspaces/{workspace_gid}/events

**Operation**: getWorkspaceEvents

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/get_workspace_events_view/get_workspace_events_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### POST /projects/{project_gid}/addCustomFieldSetting

**Operation**: addCustomFieldSettingForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/add_custom_field_setting_for_project_view/add_custom_field_setting_for_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/add_custom_field_setting_for_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### POST /projects/{project_gid}/removeCustomFieldSetting

**Operation**: removeCustomFieldSettingForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/remove_custom_field_setting_for_project_view/remove_custom_field_setting_for_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/remove_custom_field_setting_for_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### POST /projects/{project_gid}/saveAsTemplate

**Operation**: projectSaveAsTemplate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/views/project_save_as_template_view/project_save_as_template_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/interactors/project_save_as_template_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_projects/serializers.py`

### POST /tasks/{task_gid}/addDependencies

**Operation**: addDependenciesForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/add_dependencies_for_task_view/add_dependencies_for_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/add_dependencies_for_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### POST /tasks/{task_gid}/removeDependencies

**Operation**: removeDependenciesForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/remove_dependencies_for_task_view/remove_dependencies_for_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/remove_dependencies_for_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### POST /tasks/{task_gid}/addDependents

**Operation**: addDependentsForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/add_dependents_for_task_view/add_dependents_for_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/add_dependents_for_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### POST /tasks/{task_gid}/removeDependents

**Operation**: removeDependentsForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/views/remove_dependents_for_task_view/remove_dependents_for_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/interactors/remove_dependents_for_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tasks/serializers.py`

### POST /teams/{team_gid}/addUser

**Operation**: addUserForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/add_user_for_team_view/add_user_for_team_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/interactors/add_user_for_team_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### POST /teams/{team_gid}/removeUser

**Operation**: removeUserForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/views/remove_user_for_team_view/remove_user_for_team_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/interactors/remove_user_for_team_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_teams/serializers.py`

### POST /workspaces/{workspace_gid}/addUser

**Operation**: addUserForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/add_user_for_workspace_view/add_user_for_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/interactors/add_user_for_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### POST /workspaces/{workspace_gid}/removeUser

**Operation**: removeUserForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/views/remove_user_for_workspace_view/remove_user_for_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/interactors/remove_user_for_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_workspaces/serializers.py`

### POST /access_requests

**Operation**: createAccessRequest

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/views/create_access_request_view/create_access_request_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/interactors/create_access_request_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/serializers.py`

### PUT /allocations/{allocation_gid}

**Operation**: updateAllocation

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/views/update_allocation_view/update_allocation_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/interactors/update_allocation_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/serializers.py`

### POST /allocations

**Operation**: createAllocation

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/views/create_allocation_view/create_allocation_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/interactors/create_allocation_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/serializers.py`

### POST /attachments

**Operation**: createAttachmentForObject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/views/create_attachment_for_object_view/create_attachment_for_object_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/interactors/create_attachment_for_object_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/serializers.py`

### POST /budgets

**Operation**: createBudget

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/views/create_budget_view/create_budget_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/interactors/create_budget_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/serializers.py`

### PUT /budgets/{budget_gid}

**Operation**: updateBudget

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/views/update_budget_view/update_budget_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/interactors/update_budget_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/serializers.py`

### POST /custom_fields

**Operation**: createCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/create_custom_field_view/create_custom_field_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/create_custom_field_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### PUT /custom_fields/{custom_field_gid}

**Operation**: updateCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/update_custom_field_view/update_custom_field_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/update_custom_field_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### POST /custom_fields/{custom_field_gid}/enum_options

**Operation**: createEnumOptionForCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/create_enum_option_for_custom_field_view/create_enum_option_for_custom_field_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/create_enum_option_for_custom_field_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### PUT /enum_options/{enum_option_gid}

**Operation**: updateEnumOption

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/update_enum_option_view/update_enum_option_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/update_enum_option_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### POST /exports/graph

**Operation**: createGraphExport

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/views/create_graph_export_view/create_graph_export_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/interactors/create_graph_export_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/serializers.py`

### POST /exports/resource

**Operation**: createResourceExport

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/views/create_resource_export_view/create_resource_export_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/interactors/create_resource_export_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_exports/serializers.py`

### PUT /goal_relationships/{goal_relationship_gid}

**Operation**: updateGoalRelationship

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/views/update_goal_relationship_view/update_goal_relationship_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/interactors/update_goal_relationship_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/serializers.py`

### PUT /goals/{goal_gid}

**Operation**: updateGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/update_goal_view/update_goal_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/update_goal_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals

**Operation**: createGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/create_goal_view/create_goal_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/create_goal_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals/{goal_gid}/setMetric

**Operation**: createGoalMetric

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/create_goal_metric_view/create_goal_metric_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/create_goal_metric_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals/{goal_gid}/setMetricCurrentValue

**Operation**: updateGoalMetric

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/update_goal_metric_view/update_goal_metric_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/update_goal_metric_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /memberships

**Operation**: createMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/create_membership_view/create_membership_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/interactors/create_membership_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### PUT /memberships/{membership_gid}

**Operation**: updateMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/update_membership_view/update_membership_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/interactors/update_membership_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### POST /organization_exports

**Operation**: createOrganizationExport

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_organization_exports/views/create_organization_export_view/create_organization_export_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_organization_exports/interactors/create_organization_export_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_organization_exports/serializers.py`

### POST /portfolios

**Operation**: createPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/create_portfolio_view/create_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/create_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### PUT /portfolios/{portfolio_gid}

**Operation**: updatePortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/update_portfolio_view/update_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/update_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### PUT /project_briefs/{project_brief_gid}

**Operation**: updateProjectBrief

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/views/update_project_brief_view/update_project_brief_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/interactors/update_project_brief_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/serializers.py`

### POST /projects/{project_gid}/project_briefs

**Operation**: createProjectBrief

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/views/create_project_brief_view/create_project_brief_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/interactors/create_project_brief_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/serializers.py`

### POST /projects/{project_gid}/project_statuses

**Operation**: createProjectStatusForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/views/create_project_status_for_project_view/create_project_status_for_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/interactors/create_project_status_for_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/serializers.py`

### POST /rates

**Operation**: createRate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/views/create_rate_view/create_rate_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/interactors/create_rate_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/serializers.py`

### PUT /rates/{rate_gid}

**Operation**: updateRate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/views/update_rate_view/update_rate_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/interactors/update_rate_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/serializers.py`

### PUT /sections/{section_gid}

**Operation**: updateSection

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/update_section_view/update_section_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/interactors/update_section_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### POST /projects/{project_gid}/sections

**Operation**: createSectionForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/create_section_for_project_view/create_section_for_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/interactors/create_section_for_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### POST /status_updates

**Operation**: createStatusForObject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/views/create_status_for_object_view/create_status_for_object_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/interactors/create_status_for_object_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/serializers.py`

### PUT /stories/{story_gid}

**Operation**: updateStory

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/views/update_story_view/update_story_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/interactors/update_story_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/serializers.py`

### POST /tasks/{task_gid}/stories

**Operation**: createStoryForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/views/create_story_for_task_view/create_story_for_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/interactors/create_story_for_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/serializers.py`

### POST /tags

**Operation**: createTag

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/create_tag_view/create_tag_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/interactors/create_tag_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### PUT /tags/{tag_gid}

**Operation**: updateTag

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/update_tag_view/update_tag_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/interactors/update_tag_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### POST /workspaces/{workspace_gid}/tags

**Operation**: createTagForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/create_tag_for_workspace_view/create_tag_for_workspace_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/interactors/create_tag_for_workspace_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### POST /tasks/{task_gid}/time_tracking_entries

**Operation**: createTimeTrackingEntry

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/create_time_tracking_entry_view/create_time_tracking_entry_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/interactors/create_time_tracking_entry_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### PUT /time_tracking_entries/{time_tracking_entry_gid}

**Operation**: updateTimeTrackingEntry

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/update_time_tracking_entry_view/update_time_tracking_entry_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/interactors/update_time_tracking_entry_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### POST /webhooks

**Operation**: createWebhook

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/views/create_webhook_view/create_webhook_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/interactors/create_webhook_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/serializers.py`

### PUT /webhooks/{webhook_gid}

**Operation**: updateWebhook

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/views/update_webhook_view/update_webhook_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/interactors/update_webhook_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/serializers.py`

### GET /access_requests

**Operation**: getAccessRequests

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/views/get_access_requests_view/get_access_requests_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/serializers.py`

### GET /allocations/{allocation_gid}

**Operation**: getAllocation

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/views/get_allocation_view/get_allocation_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/serializers.py`

### DELETE /allocations/{allocation_gid}

**Operation**: deleteAllocation

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/views/delete_allocation_view/delete_allocation_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/interactors/delete_allocation_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/serializers.py`

### GET /allocations

**Operation**: getAllocations

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/views/get_allocations_view/get_allocations_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_allocations/serializers.py`

### GET /attachments/{attachment_gid}

**Operation**: getAttachment

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/views/get_attachment_view/get_attachment_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/serializers.py`

### DELETE /attachments/{attachment_gid}

**Operation**: deleteAttachment

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/views/delete_attachment_view/delete_attachment_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/interactors/delete_attachment_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/serializers.py`

### GET /attachments

**Operation**: getAttachmentsForObject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/views/get_attachments_for_object_view/get_attachments_for_object_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_attachments/serializers.py`

### GET /budgets

**Operation**: getBudgets

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/views/get_budgets_view/get_budgets_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/serializers.py`

### GET /budgets/{budget_gid}

**Operation**: getBudget

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/views/get_budget_view/get_budget_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/serializers.py`

### DELETE /budgets/{budget_gid}

**Operation**: deleteBudget

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/views/delete_budget_view/delete_budget_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/interactors/delete_budget_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_budgets/serializers.py`

### GET /projects/{project_gid}/custom_field_settings

**Operation**: getCustomFieldSettingsForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/views/get_custom_field_settings_for_project_view/get_custom_field_settings_for_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/serializers.py`

### GET /portfolios/{portfolio_gid}/custom_field_settings

**Operation**: getCustomFieldSettingsForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/views/get_custom_field_settings_for_portfolio_view/get_custom_field_settings_for_portfolio_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/serializers.py`

### GET /goals/{goal_gid}/custom_field_settings

**Operation**: getCustomFieldSettingsForGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/views/get_custom_field_settings_for_goal_view/get_custom_field_settings_for_goal_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/serializers.py`

### GET /teams/{team_gid}/custom_field_settings

**Operation**: getCustomFieldSettingsForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/views/get_custom_field_settings_for_team_view/get_custom_field_settings_for_team_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_field_settings/serializers.py`

### GET /custom_fields/{custom_field_gid}

**Operation**: getCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/get_custom_field_view/get_custom_field_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### DELETE /custom_fields/{custom_field_gid}

**Operation**: deleteCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/delete_custom_field_view/delete_custom_field_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/delete_custom_field_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### GET /workspaces/{workspace_gid}/custom_fields

**Operation**: getCustomFieldsForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/get_custom_fields_for_workspace_view/get_custom_fields_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### GET /custom_types

**Operation**: getCustomTypes

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_types/views/get_custom_types_view/get_custom_types_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_types/serializers.py`

### GET /custom_types/{custom_type_gid}

**Operation**: getCustomType

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_types/views/get_custom_type_view/get_custom_type_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_types/serializers.py`

### GET /events

**Operation**: getEvents

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_events/views/get_events_view/get_events_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_events/serializers.py`

### GET /goal_relationships/{goal_relationship_gid}

**Operation**: getGoalRelationship

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/views/get_goal_relationship_view/get_goal_relationship_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/serializers.py`

### GET /goal_relationships

**Operation**: getGoalRelationships

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/views/get_goal_relationships_view/get_goal_relationships_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/serializers.py`

### GET /goals/{goal_gid}

**Operation**: getGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/get_goal_view/get_goal_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### DELETE /goals/{goal_gid}

**Operation**: deleteGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/delete_goal_view/delete_goal_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/delete_goal_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### GET /goals

**Operation**: getGoals

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/get_goals_view/get_goals_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### GET /goals/{goal_gid}/parentGoals

**Operation**: getParentGoalsForGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/get_parent_goals_for_goal_view/get_parent_goals_for_goal_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### GET /jobs/{job_gid}

**Operation**: getJob

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_jobs/views/get_job_view/get_job_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_jobs/serializers.py`

### GET /memberships

**Operation**: getMemberships

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_memberships_view/get_memberships_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /memberships/{membership_gid}

**Operation**: getMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_membership_view/get_membership_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### DELETE /memberships/{membership_gid}

**Operation**: deleteMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/delete_membership_view/delete_membership_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/interactors/delete_membership_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /organization_exports/{organization_export_gid}

**Operation**: getOrganizationExport

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_organization_exports/views/get_organization_export_view/get_organization_export_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_organization_exports/serializers.py`

### GET /portfolio_memberships

**Operation**: getPortfolioMemberships

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_portfolio_memberships_view/get_portfolio_memberships_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /portfolio_memberships/{portfolio_membership_gid}

**Operation**: getPortfolioMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_portfolio_membership_view/get_portfolio_membership_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /portfolios/{portfolio_gid}/portfolio_memberships

**Operation**: getPortfolioMembershipsForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_portfolio_memberships_for_portfolio_view/get_portfolio_memberships_for_portfolio_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /portfolios

**Operation**: getPortfolios

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/get_portfolios_view/get_portfolios_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### GET /portfolios/{portfolio_gid}

**Operation**: getPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/get_portfolio_view/get_portfolio_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### DELETE /portfolios/{portfolio_gid}

**Operation**: deletePortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/delete_portfolio_view/delete_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/delete_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### GET /portfolios/{portfolio_gid}/items

**Operation**: getItemsForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/get_items_for_portfolio_view/get_items_for_portfolio_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### GET /project_briefs/{project_brief_gid}

**Operation**: getProjectBrief

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/views/get_project_brief_view/get_project_brief_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/serializers.py`

### DELETE /project_briefs/{project_brief_gid}

**Operation**: deleteProjectBrief

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/views/delete_project_brief_view/delete_project_brief_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/interactors/delete_project_brief_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_briefs/serializers.py`

### GET /project_memberships/{project_membership_gid}

**Operation**: getProjectMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_project_membership_view/get_project_membership_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /projects/{project_gid}/project_memberships

**Operation**: getProjectMembershipsForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_project_memberships_for_project_view/get_project_memberships_for_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /project_statuses/{project_status_gid}

**Operation**: getProjectStatus

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/views/get_project_status_view/get_project_status_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/serializers.py`

### DELETE /project_statuses/{project_status_gid}

**Operation**: deleteProjectStatus

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/views/delete_project_status_view/delete_project_status_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/interactors/delete_project_status_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/serializers.py`

### GET /projects/{project_gid}/project_statuses

**Operation**: getProjectStatusesForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/views/get_project_statuses_for_project_view/get_project_statuses_for_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_statuses/serializers.py`

### GET /project_templates/{project_template_gid}

**Operation**: getProjectTemplate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/views/get_project_template_view/get_project_template_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/serializers.py`

### DELETE /project_templates/{project_template_gid}

**Operation**: deleteProjectTemplate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/views/delete_project_template_view/delete_project_template_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/interactors/delete_project_template_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/serializers.py`

### GET /project_templates

**Operation**: getProjectTemplates

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/views/get_project_templates_view/get_project_templates_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/serializers.py`

### GET /teams/{team_gid}/project_templates

**Operation**: getProjectTemplatesForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/views/get_project_templates_for_team_view/get_project_templates_for_team_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/serializers.py`

### GET /rates

**Operation**: getRates

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/views/get_rates_view/get_rates_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/serializers.py`

### GET /rates/{rate_gid}

**Operation**: getRate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/views/get_rate_view/get_rate_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/serializers.py`

### DELETE /rates/{rate_gid}

**Operation**: deleteRate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/views/delete_rate_view/delete_rate_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/interactors/delete_rate_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rates/serializers.py`

### GET /reactions

**Operation**: getReactionsOnObject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_reactions/views/get_reactions_on_object_view/get_reactions_on_object_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_reactions/serializers.py`

### GET /sections/{section_gid}

**Operation**: getSection

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/get_section_view/get_section_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### DELETE /sections/{section_gid}

**Operation**: deleteSection

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/delete_section_view/delete_section_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/interactors/delete_section_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### GET /projects/{project_gid}/sections

**Operation**: getSectionsForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/get_sections_for_project_view/get_sections_for_project_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### GET /status_updates/{status_update_gid}

**Operation**: getStatus

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/views/get_status_view/get_status_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/serializers.py`

### DELETE /status_updates/{status_update_gid}

**Operation**: deleteStatus

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/views/delete_status_view/delete_status_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/interactors/delete_status_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/serializers.py`

### GET /status_updates

**Operation**: getStatusesForObject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/views/get_statuses_for_object_view/get_statuses_for_object_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_status_updates/serializers.py`

### GET /stories/{story_gid}

**Operation**: getStory

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/views/get_story_view/get_story_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/serializers.py`

### DELETE /stories/{story_gid}

**Operation**: deleteStory

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/views/delete_story_view/delete_story_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/interactors/delete_story_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/serializers.py`

### GET /tasks/{task_gid}/stories

**Operation**: getStoriesForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/views/get_stories_for_task_view/get_stories_for_task_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_stories/serializers.py`

### GET /tags

**Operation**: getTags

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/get_tags_view/get_tags_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### GET /tags/{tag_gid}

**Operation**: getTag

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/get_tag_view/get_tag_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### DELETE /tags/{tag_gid}

**Operation**: deleteTag

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/delete_tag_view/delete_tag_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/interactors/delete_tag_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### GET /tasks/{task_gid}/tags

**Operation**: getTagsForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/get_tags_for_task_view/get_tags_for_task_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### GET /workspaces/{workspace_gid}/tags

**Operation**: getTagsForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/views/get_tags_for_workspace_view/get_tags_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_tags/serializers.py`

### GET /task_templates

**Operation**: getTaskTemplates

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/views/get_task_templates_view/get_task_templates_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/serializers.py`

### GET /task_templates/{task_template_gid}

**Operation**: getTaskTemplate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/views/get_task_template_view/get_task_template_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/serializers.py`

### DELETE /task_templates/{task_template_gid}

**Operation**: deleteTaskTemplate

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/views/delete_task_template_view/delete_task_template_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/interactors/delete_task_template_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/serializers.py`

### GET /team_memberships/{team_membership_gid}

**Operation**: getTeamMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_team_membership_view/get_team_membership_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /team_memberships

**Operation**: getTeamMemberships

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_team_memberships_view/get_team_memberships_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /teams/{team_gid}/team_memberships

**Operation**: getTeamMembershipsForTeam

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_team_memberships_for_team_view/get_team_memberships_for_team_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /users/{user_gid}/team_memberships

**Operation**: getTeamMembershipsForUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_team_memberships_for_user_view/get_team_memberships_for_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /time_periods/{time_period_gid}

**Operation**: getTimePeriod

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_periods/views/get_time_period_view/get_time_period_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_periods/serializers.py`

### GET /time_periods

**Operation**: getTimePeriods

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_periods/views/get_time_periods_view/get_time_periods_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_periods/serializers.py`

### GET /tasks/{task_gid}/time_tracking_entries

**Operation**: getTimeTrackingEntriesForTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/get_time_tracking_entries_for_task_view/get_time_tracking_entries_for_task_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### GET /time_tracking_entries/{time_tracking_entry_gid}

**Operation**: getTimeTrackingEntry

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/get_time_tracking_entry_view/get_time_tracking_entry_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### DELETE /time_tracking_entries/{time_tracking_entry_gid}

**Operation**: deleteTimeTrackingEntry

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/delete_time_tracking_entry_view/delete_time_tracking_entry_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/interactors/delete_time_tracking_entry_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### GET /time_tracking_entries

**Operation**: getTimeTrackingEntries

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/views/get_time_tracking_entries_view/get_time_tracking_entries_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_time_tracking/serializers.py`

### GET /user_task_lists/{user_task_list_gid}

**Operation**: getUserTaskList

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_user_task_lists/views/get_user_task_list_view/get_user_task_list_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_user_task_lists/serializers.py`

### GET /users/{user_gid}/user_task_list

**Operation**: getUserTaskListForUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_user_task_lists/views/get_user_task_list_for_user_view/get_user_task_list_for_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_user_task_lists/serializers.py`

### GET /webhooks

**Operation**: getWebhooks

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/views/get_webhooks_view/get_webhooks_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/serializers.py`

### GET /webhooks/{webhook_gid}

**Operation**: getWebhook

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/views/get_webhook_view/get_webhook_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/serializers.py`

### DELETE /webhooks/{webhook_gid}

**Operation**: deleteWebhook

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/views/delete_webhook_view/delete_webhook_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/interactors/delete_webhook_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_webhooks/serializers.py`

### GET /workspace_memberships/{workspace_membership_gid}

**Operation**: getWorkspaceMembership

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_workspace_membership_view/get_workspace_membership_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /users/{user_gid}/workspace_memberships

**Operation**: getWorkspaceMembershipsForUser

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_workspace_memberships_for_user_view/get_workspace_memberships_for_user_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### GET /workspaces/{workspace_gid}/workspace_memberships

**Operation**: getWorkspaceMembershipsForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/views/get_workspace_memberships_for_workspace_view/get_workspace_memberships_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_memberships/serializers.py`

### POST /custom_fields/{custom_field_gid}/enum_options/insert

**Operation**: insertEnumOptionForCustomField

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/views/insert_enum_option_for_custom_field_view/insert_enum_option_for_custom_field_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/interactors/insert_enum_option_for_custom_field_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_custom_fields/serializers.py`

### POST /goals/{goal_gid}/addSupportingRelationship

**Operation**: addSupportingRelationship

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/views/add_supporting_relationship_view/add_supporting_relationship_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/interactors/add_supporting_relationship_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/serializers.py`

### POST /goals/{goal_gid}/removeSupportingRelationship

**Operation**: removeSupportingRelationship

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/views/remove_supporting_relationship_view/remove_supporting_relationship_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/interactors/remove_supporting_relationship_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goal_relationships/serializers.py`

### POST /goals/{goal_gid}/addFollowers

**Operation**: addFollowers

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/add_followers_view/add_followers_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/add_followers_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals/{goal_gid}/removeFollowers

**Operation**: removeFollowers

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/remove_followers_view/remove_followers_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/remove_followers_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals/{goal_gid}/addCustomFieldSetting

**Operation**: addCustomFieldSettingForGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/add_custom_field_setting_for_goal_view/add_custom_field_setting_for_goal_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/add_custom_field_setting_for_goal_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /goals/{goal_gid}/removeCustomFieldSetting

**Operation**: removeCustomFieldSettingForGoal

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/views/remove_custom_field_setting_for_goal_view/remove_custom_field_setting_for_goal_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/interactors/remove_custom_field_setting_for_goal_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_goals/serializers.py`

### POST /portfolios/{portfolio_gid}/addItem

**Operation**: addItemForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/add_item_for_portfolio_view/add_item_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/add_item_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /portfolios/{portfolio_gid}/removeItem

**Operation**: removeItemForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/remove_item_for_portfolio_view/remove_item_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/remove_item_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /portfolios/{portfolio_gid}/addCustomFieldSetting

**Operation**: addCustomFieldSettingForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/add_custom_field_setting_for_portfolio_view/add_custom_field_setting_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/add_custom_field_setting_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /portfolios/{portfolio_gid}/removeCustomFieldSetting

**Operation**: removeCustomFieldSettingForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/remove_custom_field_setting_for_portfolio_view/remove_custom_field_setting_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/remove_custom_field_setting_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /portfolios/{portfolio_gid}/addMembers

**Operation**: addMembersForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/add_members_for_portfolio_view/add_members_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/add_members_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /portfolios/{portfolio_gid}/removeMembers

**Operation**: removeMembersForPortfolio

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/views/remove_members_for_portfolio_view/remove_members_for_portfolio_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/interactors/remove_members_for_portfolio_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_portfolios/serializers.py`

### POST /project_templates/{project_template_gid}/instantiateProject

**Operation**: instantiateProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/views/instantiate_project_view/instantiate_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/interactors/instantiate_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_project_templates/serializers.py`

### POST /rule_triggers/{rule_trigger_gid}/run

**Operation**: triggerRule

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_rules/views/trigger_rule_view/trigger_rule_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_rules/interactors/trigger_rule_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_rules/serializers.py`

### POST /sections/{section_gid}/addTask

**Operation**: addTaskForSection

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/add_task_for_section_view/add_task_for_section_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/interactors/add_task_for_section_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### POST /projects/{project_gid}/sections/insert

**Operation**: insertSectionForProject

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/views/insert_section_for_project_view/insert_section_for_project_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/interactors/insert_section_for_project_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_sections/serializers.py`

### POST /task_templates/{task_template_gid}/instantiateTask

**Operation**: instantiateTask

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/views/instantiate_task_view/instantiate_task_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/interactors/instantiate_task_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_task_templates/serializers.py`

### POST /access_requests/{access_request_gid}/approve

**Operation**: approveAccessRequest

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/views/approve_access_request_view/approve_access_request_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/interactors/approve_access_request_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/serializers.py`

### POST /access_requests/{access_request_gid}/reject

**Operation**: rejectAccessRequest

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/views/reject_access_request_view/reject_access_request_view.py`
- interactor: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/interactors/reject_access_request_interactor.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_access_requests/serializers.py`

### GET /workspaces/{workspace_gid}/typeahead

**Operation**: typeaheadForWorkspace

**Files Generated**:

- view: `/home/nxtwave/study/scalar_assignment/backend/asana_typeahead/views/typeahead_for_workspace_view/typeahead_for_workspace_view.py`
- serializer: `/home/nxtwave/study/scalar_assignment/backend/asana_typeahead/serializers.py`

## Next Steps

After code generation, you need to:

1. **Update URLs**: Add new view imports and URL patterns
2. **Run Migrations**: If new models were created
3. **Implement Logic**: Complete TODOs in generated code
4. **Add Tests**: Create test cases for new endpoints
5. **Review Code**: Ensure it follows project standards
