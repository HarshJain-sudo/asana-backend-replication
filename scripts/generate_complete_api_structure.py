#!/usr/bin/env python3
"""
Comprehensive script to generate all missing API structures following Clean Architecture.
This will create models, serializers, interactors, storages, presenters, and views for all missing APIs.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# All missing APIs organized by priority
PHASE_1_APIS = {
    'workspaces': [
        ('PUT', '/workspaces/{workspace_gid}', 'update_workspace'),
        ('POST', '/workspaces/{workspace_gid}/addUser', 'add_user_to_workspace'),
        ('POST', '/workspaces/{workspace_gid}/removeUser', 'remove_user_from_workspace'),
        ('GET', '/workspaces/{workspace_gid}/events', 'get_workspace_events'),
    ],
    'teams': [
        ('POST', '/teams', 'create_team'),
        ('PUT', '/teams/{team_gid}', 'update_team'),
        ('POST', '/teams/{team_gid}/addUser', 'add_user_to_team'),
        ('POST', '/teams/{team_gid}/removeUser', 'remove_user_from_team'),
        ('GET', '/users/{user_gid}/teams', 'get_teams_for_user'),
    ],
    'tags': [
        ('POST', '/tags', 'create_tag'),
        ('PUT', '/tags/{tag_gid}', 'update_tag'),
        ('DELETE', '/tags/{tag_gid}', 'delete_tag'),
        ('POST', '/workspaces/{workspace_gid}/tags', 'create_tag_in_workspace'),
        ('GET', '/tasks/{task_gid}/tags', 'get_task_tags'),
    ],
    'tasks': [
        ('POST', '/tasks/{task_gid}/duplicate', 'duplicate_task'),
        ('GET', '/tasks/{task_gid}/dependencies', 'get_task_dependencies'),
        ('POST', '/tasks/{task_gid}/dependencies', 'set_task_dependencies'),
        ('POST', '/tasks/{task_gid}/dependencies/remove', 'remove_task_dependencies'),
        ('GET', '/tasks/{task_gid}/dependents', 'get_task_dependents'),
        ('POST', '/tasks/{task_gid}/dependents', 'set_task_dependents'),
        ('POST', '/tasks/{task_gid}/dependents/remove', 'remove_task_dependents'),
        ('GET', '/tasks/{custom_id}', 'get_task_by_custom_id'),
    ],
    'projects': [
        ('GET', '/projects/{project_gid}/taskCount', 'get_project_task_count'),
        ('POST', '/projects/{project_gid}/addCustomField', 'add_custom_field_to_project'),
        ('POST', '/projects/{project_gid}/removeCustomField', 'remove_custom_field_from_project'),
    ],
    'stories': [
        ('PUT', '/stories/{story_gid}', 'update_story'),
        ('DELETE', '/stories/{story_gid}', 'delete_story'),
    ],
    'attachments': [
        ('DELETE', '/attachments/{attachment_gid}', 'delete_attachment'),
        ('POST', '/attachments', 'upload_attachment'),
        ('GET', '/attachments', 'get_attachments_from_object'),
    ],
}

PHASE_2_APIS = {
    'sections': [
        ('GET', '/sections/{section_gid}', 'get_section'),
        ('PUT', '/sections/{section_gid}', 'update_section'),
        ('DELETE', '/sections/{section_gid}', 'delete_section'),
        ('GET', '/projects/{project_gid}/sections', 'get_project_sections'),
        ('POST', '/projects/{project_gid}/sections', 'create_section'),
        ('POST', '/sections/{section_gid}/addTask', 'add_task_to_section'),
        ('POST', '/sections/{section_gid}/insert', 'move_insert_sections'),
    ],
    'project_statuses': [
        ('GET', '/project_statuses/{project_status_gid}', 'get_project_status'),
        ('DELETE', '/project_statuses/{project_status_gid}', 'delete_project_status'),
        ('GET', '/projects/{project_gid}/project_statuses', 'get_project_statuses'),
        ('POST', '/projects/{project_gid}/project_statuses', 'create_project_status'),
    ],
    'project_briefs': [
        ('GET', '/project_briefs/{project_brief_gid}', 'get_project_brief'),
        ('PUT', '/project_briefs/{project_brief_gid}', 'update_project_brief'),
        ('DELETE', '/project_briefs/{project_brief_gid}', 'delete_project_brief'),
        ('POST', '/projects/{project_gid}/project_brief', 'create_project_brief'),
    ],
    'user_task_lists': [
        ('GET', '/user_task_lists/{user_task_list_gid}', 'get_user_task_list'),
        ('GET', '/users/{user_gid}/user_task_list', 'get_users_task_list'),
    ],
}

print("API Structure Generator")
print("=" * 60)
print(f"Phase 1 APIs: {sum(len(apis) for apis in PHASE_1_APIS.values())} endpoints")
print(f"Phase 2 APIs: {sum(len(apis) for apis in PHASE_2_APIS.values())} endpoints")
print("=" * 60)

