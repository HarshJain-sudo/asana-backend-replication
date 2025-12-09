# API Comparison Report

Generated: 2025-12-10 01:25:02

## Summary

- **Total endpoints in OpenAPI spec**: 217
- **Total endpoints implemented**: 24
- **Missing endpoints**: 193
- **Extra endpoints**: 4
- **Coverage**: 11.06%

## Priority Distribution

- **High Priority** (≥70): 83
- **Medium Priority** (40-69): 110
- **Low Priority** (<40): 0

## Missing APIs by Resource

- **projects**: 12 missing
- **goals**: 12 missing
- **portfolios**: 12 missing
- **tasks**: 10 missing
- **users**: 8 missing
- **custom fields**: 8 missing
- **tags**: 8 missing
- **teams**: 7 missing
- **sections**: 7 missing
- **workspaces**: 6 missing
- **time tracking entries**: 6 missing
- **allocations**: 5 missing
- **budgets**: 5 missing
- **goal relationships**: 5 missing
- **memberships**: 5 missing
- **rates**: 5 missing
- **stories**: 5 missing
- **webhooks**: 5 missing
- **project templates**: 5 missing
- **access requests**: 4 missing
- **attachments**: 4 missing
- **project briefs**: 4 missing
- **project statuses**: 4 missing
- **status updates**: 4 missing
- **custom field settings**: 4 missing
- **task templates**: 4 missing
- **team memberships**: 4 missing
- **portfolio memberships**: 3 missing
- **workspace memberships**: 3 missing
- **exports**: 2 missing
- **organization exports**: 2 missing
- **custom types**: 2 missing
- **project memberships**: 2 missing
- **time periods**: 2 missing
- **user task lists**: 2 missing
- **batch api**: 1 missing
- **audit log api**: 1 missing
- **events**: 1 missing
- **jobs**: 1 missing
- **reactions**: 1 missing
- **rules**: 1 missing
- **typeahead**: 1 missing

## Missing APIs Details

### High Priority

#### POST /projects

- **Operation**: createProject
- **Summary**: Create a project...
- **Resource**: projects
- **Priority**: 95/100
- **Query Params**: opt_pretty, opt_fields

#### PUT /projects/{project_gid}

- **Operation**: updateProject
- **Summary**: Update a project...
- **Resource**: projects
- **Priority**: 95/100
- **Path Params**: project_gid
- **Query Params**: opt_pretty, opt_fields

#### POST /teams/{team_gid}/projects

- **Operation**: createProjectForTeam
- **Summary**: Create a project in a team...
- **Resource**: projects
- **Priority**: 95/100
- **Path Params**: team_gid
- **Query Params**: opt_pretty, opt_fields

#### POST /workspaces/{workspace_gid}/projects

- **Operation**: createProjectForWorkspace
- **Summary**: Create a project in a workspace...
- **Resource**: projects
- **Priority**: 95/100
- **Path Params**: workspace_gid
- **Query Params**: opt_pretty, opt_fields

#### PUT /tasks/{task_gid}

- **Operation**: updateTask
- **Summary**: Update a task...
- **Resource**: tasks
- **Priority**: 95/100
- **Path Params**: task_gid
- **Query Params**: opt_pretty, opt_fields

#### POST /teams

- **Operation**: createTeam
- **Summary**: Create a team...
- **Resource**: teams
- **Priority**: 95/100
- **Query Params**: opt_pretty, opt_fields

#### PUT /teams/{team_gid}

- **Operation**: updateTeam
- **Summary**: Update a team...
- **Resource**: teams
- **Priority**: 95/100
- **Path Params**: team_gid
- **Query Params**: opt_pretty, opt_fields

#### PUT /users/{user_gid}

- **Operation**: updateUser
- **Summary**: Update a user...
- **Resource**: users
- **Priority**: 95/100
- **Path Params**: user_gid
- **Query Params**: opt_pretty, workspace, opt_fields

#### PUT /workspaces/{workspace_gid}/users/{user_gid}

- **Operation**: updateUserForWorkspace
- **Summary**: Update a user in a workspace or organization...
- **Resource**: users
- **Priority**: 95/100
- **Path Params**: workspace_gid, user_gid
- **Query Params**: opt_pretty, opt_fields

#### PUT /workspaces/{workspace_gid}

- **Operation**: updateWorkspace
- **Summary**: Update a workspace...
- **Resource**: workspaces
- **Priority**: 95/100
- **Path Params**: workspace_gid
- **Query Params**: opt_pretty, opt_fields

#### GET /projects

- **Operation**: getProjects
- **Summary**: Get multiple projects...
- **Resource**: projects
- **Priority**: 85/100
- **Query Params**: opt_pretty, limit, offset, workspace, team

#### GET /projects/{project_gid}

- **Operation**: getProject
- **Summary**: Get a project...
- **Resource**: projects
- **Priority**: 85/100
- **Path Params**: project_gid
- **Query Params**: opt_pretty, opt_fields

#### DELETE /projects/{project_gid}

- **Operation**: deleteProject
- **Summary**: Delete a project...
- **Resource**: projects
- **Priority**: 85/100
- **Path Params**: project_gid
- **Query Params**: opt_pretty

#### GET /tasks/{task_gid}/projects

- **Operation**: getProjectsForTask
- **Summary**: Get projects a task is in...
- **Resource**: projects
- **Priority**: 85/100
- **Path Params**: task_gid
- **Query Params**: opt_pretty, limit, offset, opt_fields

#### GET /projects/{project_gid}/task_counts

- **Operation**: getTaskCountsForProject
- **Summary**: Get task count of a project...
- **Resource**: projects
- **Priority**: 85/100
- **Path Params**: project_gid
- **Query Params**: opt_pretty, opt_fields

#### DELETE /tasks/{task_gid}

- **Operation**: deleteTask
- **Summary**: Delete a task...
- **Resource**: tasks
- **Priority**: 85/100
- **Path Params**: task_gid
- **Query Params**: opt_pretty

#### GET /sections/{section_gid}/tasks

- **Operation**: getTasksForSection
- **Summary**: Get tasks from a section...
- **Resource**: tasks
- **Priority**: 85/100
- **Path Params**: section_gid
- **Query Params**: opt_pretty, limit, offset, completed_since, opt_fields

#### GET /tags/{tag_gid}/tasks

- **Operation**: getTasksForTag
- **Summary**: Get tasks from a tag...
- **Resource**: tasks
- **Priority**: 85/100
- **Path Params**: tag_gid
- **Query Params**: opt_pretty, limit, offset, opt_fields

#### GET /user_task_lists/{user_task_list_gid}/tasks

- **Operation**: getTasksForUserTaskList
- **Summary**: Get tasks from a user task list...
- **Resource**: tasks
- **Priority**: 85/100
- **Path Params**: user_task_list_gid
- **Query Params**: completed_since, opt_pretty, limit, offset, opt_fields

#### GET /workspaces/{workspace_gid}/tasks/custom_id/{custom_id}

- **Operation**: getTaskForCustomID
- **Summary**: Get a task for a given custom ID...
- **Resource**: tasks
- **Priority**: 85/100
- **Path Params**: workspace_gid, custom_id

### Medium Priority

#### GET /access_requests

- **Operation**: getAccessRequests
- **Summary**: Get access requests...
- **Resource**: access requests
- **Priority**: 65/100
- **Query Params**: target, user, opt_pretty, opt_fields

#### GET /allocations/{allocation_gid}

- **Operation**: getAllocation
- **Summary**: Get an allocation...
- **Resource**: allocations
- **Priority**: 65/100
- **Path Params**: allocation_gid
- **Query Params**: opt_pretty, opt_fields

#### DELETE /allocations/{allocation_gid}

- **Operation**: deleteAllocation
- **Summary**: Delete an allocation...
- **Resource**: allocations
- **Priority**: 65/100
- **Path Params**: allocation_gid
- **Query Params**: opt_pretty

#### GET /allocations

- **Operation**: getAllocations
- **Summary**: Get multiple allocations...
- **Resource**: allocations
- **Priority**: 65/100
- **Query Params**: opt_pretty, parent, assignee, workspace, limit

#### GET /attachments/{attachment_gid}

- **Operation**: getAttachment
- **Summary**: Get an attachment...
- **Resource**: attachments
- **Priority**: 65/100
- **Path Params**: attachment_gid
- **Query Params**: opt_pretty, opt_fields

#### DELETE /attachments/{attachment_gid}

- **Operation**: deleteAttachment
- **Summary**: Delete an attachment...
- **Resource**: attachments
- **Priority**: 65/100
- **Path Params**: attachment_gid
- **Query Params**: opt_pretty

#### GET /attachments

- **Operation**: getAttachmentsForObject
- **Summary**: Get attachments from an object...
- **Resource**: attachments
- **Priority**: 65/100
- **Query Params**: opt_pretty, limit, offset, parent, opt_fields

#### GET /workspaces/{workspace_gid}/audit_log_events

- **Operation**: getAuditLogEvents
- **Summary**: Get audit log events...
- **Resource**: audit log api
- **Priority**: 65/100
- **Path Params**: workspace_gid
- **Query Params**: start_at, end_at, event_type, actor_type, actor_gid

#### GET /budgets

- **Operation**: getBudgets
- **Summary**: Get all budgets...
- **Resource**: budgets
- **Priority**: 65/100
- **Query Params**: opt_pretty, parent

#### GET /budgets/{budget_gid}

- **Operation**: getBudget
- **Summary**: Get a budget...
- **Resource**: budgets
- **Priority**: 65/100
- **Path Params**: budget_gid
- **Query Params**: opt_pretty, opt_fields

#### DELETE /budgets/{budget_gid}

- **Operation**: deleteBudget
- **Summary**: Delete a budget...
- **Resource**: budgets
- **Priority**: 65/100
- **Path Params**: budget_gid
- **Query Params**: opt_pretty

#### GET /projects/{project_gid}/custom_field_settings

- **Operation**: getCustomFieldSettingsForProject
- **Summary**: Get a project's custom fields...
- **Resource**: custom field settings
- **Priority**: 65/100
- **Path Params**: project_gid
- **Query Params**: opt_pretty, limit, offset, opt_fields

#### GET /portfolios/{portfolio_gid}/custom_field_settings

- **Operation**: getCustomFieldSettingsForPortfolio
- **Summary**: Get a portfolio's custom fields...
- **Resource**: custom field settings
- **Priority**: 65/100
- **Path Params**: portfolio_gid
- **Query Params**: opt_pretty, limit, offset, opt_fields

#### GET /goals/{goal_gid}/custom_field_settings

- **Operation**: getCustomFieldSettingsForGoal
- **Summary**: Get a goal's custom fields...
- **Resource**: custom field settings
- **Priority**: 65/100
- **Path Params**: goal_gid
- **Query Params**: opt_pretty, limit, offset, opt_fields

#### GET /teams/{team_gid}/custom_field_settings

- **Operation**: getCustomFieldSettingsForTeam
- **Summary**: Get a team's custom fields...
- **Resource**: custom field settings
- **Priority**: 65/100
- **Path Params**: team_gid
- **Query Params**: opt_pretty, opt_fields

## Extra APIs (Not in Spec)

- `POST /tasks/{task_gid}/dependencies` (asana_tasks)
- `POST /tasks/{task_gid}/dependencies/remove` (asana_tasks)
- `POST /tasks/{task_gid}/dependents` (asana_tasks)
- `POST /tasks/{task_gid}/dependents/remove` (asana_tasks)
