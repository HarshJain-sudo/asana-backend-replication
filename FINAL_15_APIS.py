#!/usr/bin/env python3
"""
===============================================================================
                    FINAL 15 APIs FOR EVALUATION
        Complete Test Suite with Success and Error Response Cases
===============================================================================

This file contains the 15 APIs for evaluation testing, covering:
- Basic CRUD operations
- Complex relationship operations (subtasks, parent-child)
- Advanced search with multiple filters
- All edge cases with proper error responses

Base URL: http://localhost:8000/api/1.0
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8000/api/1.0"


def print_response(name, response):
    """Pretty print API response"""
    print(f"\n{'='*70}")
    print(f"API: {name}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print('='*70)


# ============================================================================
#                           15 APIs FOR EVALUATION
# ============================================================================

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #1: GET /workspaces/                            ║
║                        Get all workspaces                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/workspaces/
Description: Returns all workspaces the user has access to.

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "951305cb-a345-49b2-9441-07698160a4e1",
            "resource_type": "workspace",
            "name": "Engineering Workspace",
            "is_organization": true
        }
    ]
}

EDGE CASES:
- Empty workspace list: Returns {"data": []}
- Pagination: Use ?limit=10&offset=0
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #2: GET /workspaces/{gid}/                      ║
║                        Get a single workspace                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/workspaces/{workspace_gid}/
Description: Returns the full workspace record for a single workspace.

SUCCESS RESPONSE (200):
{
    "data": {
        "gid": "951305cb-a345-49b2-9441-07698160a4e1",
        "resource_type": "workspace",
        "name": "Engineering Workspace",
        "is_organization": true,
        "created_at": "2025-12-09T11:14:27.672114+00:00"
    }
}

ERROR RESPONSES:

404 Not Found - Workspace doesn't exist:
{
    "errors": [{"message": "Workspace does not exist"}]
}

400 Bad Request - Invalid GID format:
{
    "errors": [{"message": "Invalid workspace GID format"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #3: GET /tasks/                                 ║
║                        Get multiple tasks                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/tasks/
Description: Returns tasks with optional filters.

QUERY PARAMETERS:
- workspace: UUID of workspace
- assignee: UUID of user
- completed: true/false
- limit: 1-100 (default: 50)
- offset: 0+ (default: 0)

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "12345678-1234-1234-1234-123456789012",
            "resource_type": "task",
            "name": "Build API",
            "completed": false,
            "assignee": {
                "gid": "user-gid",
                "resource_type": "user",
                "name": "John Doe"
            }
        }
    ]
}

ERROR RESPONSES:

400 Bad Request - Invalid pagination:
{
    "errors": [{"message": "limit must be between 1 and 100"}]
}

400 Bad Request - Negative offset:
{
    "errors": [{"message": "offset must be >= 0"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #4: POST /tasks/                                ║
║                        Create a task                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: POST /api/1.0/tasks/
Description: Creates a new task in a workspace.

REQUEST BODY:
{
    "data": {
        "name": "New Task",
        "workspace": "workspace-gid",
        "assignee": "user-gid",       // optional
        "due_on": "2025-12-31",        // optional
        "notes": "Task description"    // optional
    }
}

SUCCESS RESPONSE (201):
{
    "data": {
        "gid": "new-task-gid",
        "resource_type": "task",
        "name": "New Task",
        "completed": false,
        "workspace": {
            "gid": "workspace-gid",
            "resource_type": "workspace",
            "name": "Workspace Name"
        }
    }
}

ERROR RESPONSES:

400 Bad Request - Missing required field:
{
    "errors": [{"message": "name: Missing required field"}]
}

400 Bad Request - Invalid workspace:
{
    "errors": [{"message": "Workspace does not exist"}]
}

400 Bad Request - Invalid date format:
{
    "errors": [{"message": "due_on: Invalid date format. Use YYYY-MM-DD"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #5: GET /tasks/{task_gid}/                      ║
║                        Get a task                                          ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/tasks/{task_gid}/
Description: Returns the complete task record for a single task.

SUCCESS RESPONSE (200):
{
    "data": {
        "gid": "task-gid",
        "resource_type": "task",
        "name": "Task Name",
        "completed": false,
        "due_on": "2025-12-31",
        "notes": "Task description",
        "workspace": {"gid": "...", "resource_type": "workspace", "name": "..."},
        "assignee": {"gid": "...", "resource_type": "user", "name": "..."} | null,
        "parent": {"gid": "...", "resource_type": "task", "name": "..."} | null,
        "num_subtasks": 0,
        "created_at": "2025-12-09T10:00:00Z",
        "modified_at": "2025-12-09T10:00:00Z"
    }
}

ERROR RESPONSES:

404 Not Found:
{
    "errors": [{"message": "Task does not exist"}]
}

400 Bad Request:
{
    "errors": [{"message": "Invalid task GID format"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #6: PUT /tasks/{task_gid}/                      ║
║                        Update a task                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: PUT /api/1.0/tasks/{task_gid}/
Description: Updates an existing task.

REQUEST BODY:
{
    "data": {
        "name": "Updated Name",
        "completed": true,
        "due_on": "2025-12-31"
    }
}

SUCCESS RESPONSE (200):
{
    "data": {
        "gid": "task-gid",
        "resource_type": "task",
        "name": "Updated Name",
        "completed": true,
        "completed_at": "2025-12-09T10:00:00Z"
    }
}

ERROR RESPONSES:

404 Not Found:
{
    "errors": [{"message": "Task does not exist"}]
}

400 Bad Request - Read-only field:
{
    "errors": [{"message": "workspace: Cannot modify read-only field"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #7: DELETE /tasks/{task_gid}/                   ║
║                        Delete a task                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: DELETE /api/1.0/tasks/{task_gid}/
Description: Deletes a task permanently.

SUCCESS RESPONSE (200):
{
    "data": {}
}

ERROR RESPONSES:

404 Not Found:
{
    "errors": [{"message": "Task does not exist"}]
}

400 Bad Request:
{
    "errors": [{"message": "Invalid task GID format"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    API #8: GET /tasks/{task_gid}/subtasks/                 ║
║                    Get subtasks from a task                                ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/tasks/{task_gid}/subtasks/
Description: Returns all subtasks of a task.

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "subtask-gid",
            "resource_type": "task",
            "name": "Subtask 1",
            "resource_subtype": "default_task",
            "completed": false
        }
    ]
}

ERROR RESPONSES:

404 Not Found - Parent task doesn't exist:
{
    "errors": [{"message": "task: Unknown object: invalid-gid"}]
}

400 Bad Request - Invalid limit:
{
    "errors": [{"message": "limit must be between 1 and 100"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   API #9: POST /tasks/{task_gid}/subtasks/                 ║
║                   Create a subtask                                         ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: POST /api/1.0/tasks/{task_gid}/subtasks/
Description: Creates a new subtask for the given task.

REQUEST BODY:
{
    "data": {
        "name": "New Subtask",
        "notes": "Subtask description"
    }
}

SUCCESS RESPONSE (201):
{
    "data": {
        "gid": "new-subtask-gid",
        "resource_type": "task",
        "name": "New Subtask",
        "parent": {
            "gid": "parent-task-gid",
            "resource_type": "task",
            "name": "Parent Task"
        }
    }
}

ERROR RESPONSES:

400 Bad Request - Missing name:
{
    "errors": [{"message": "name: Missing required field"}]
}

404 Not Found - Parent doesn't exist:
{
    "errors": [{"message": "task: Unknown object: invalid-gid"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   API #10: POST /tasks/{task_gid}/setParent/               ║
║                   Set the parent of a task                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: POST /api/1.0/tasks/{task_gid}/setParent/
Description: Changes the parent of a task (makes it a subtask or top-level).

REQUEST BODY:
{
    "data": {
        "parent": "parent-task-gid"     // or null for no parent
    }
}

SUCCESS RESPONSE (200):
{
    "data": {
        "gid": "task-gid",
        "resource_type": "task",
        "name": "Task Name",
        "parent": {
            "gid": "parent-gid",
            "resource_type": "task",
            "name": "Parent Task"
        }
    }
}

ERROR RESPONSES:

400 Bad Request - Circular reference:
{
    "errors": [{"message": "Cannot set a task as its own parent"}]
}

400 Bad Request - Circular hierarchy:
{
    "errors": [{"message": "Cannot create circular reference in task hierarchy"}]
}

404 Not Found:
{
    "errors": [{"message": "parent: Unknown object: invalid-gid"}]
}

400 Bad Request - Different workspace:
{
    "errors": [{"message": "Parent task must be in the same workspace"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║            API #11: GET /workspaces/{workspace_gid}/tasks/search/          ║
║            Search tasks in a workspace                                     ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/workspaces/{workspace_gid}/tasks/search/
Description: Full-text search on task name and description with filters.

QUERY PARAMETERS:
- text: Search query (searches name and notes)
- resource_subtype: default_task | milestone | approval
- completed: true | false
- is_subtask: true | false
- due_on.before: YYYY-MM-DD
- due_on.after: YYYY-MM-DD

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "task-gid",
            "resource_type": "task",
            "name": "Bug fix",
            "resource_subtype": "default_task",
            "completed": false
        }
    ]
}

ERROR RESPONSES:

404 Not Found - Workspace doesn't exist:
{
    "errors": [{"message": "workspace: Unknown object: invalid-gid"}]
}

400 Bad Request - Invalid date:
{
    "errors": [{"message": "due_on.before: Invalid date format. Use YYYY-MM-DD"}]
}

400 Bad Request - Invalid resource_subtype:
{
    "errors": [{"message": "resource_subtype: Invalid value. Use default_task, milestone, or approval"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  API #12: POST /tasks/{task_gid}/addProject/               ║
║                  Add a project to a task                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: POST /api/1.0/tasks/{task_gid}/addProject/
Description: Adds a project to a task.

REQUEST BODY:
{
    "data": {
        "project": "project-gid"
    }
}

SUCCESS RESPONSE (200):
{
    "data": {}
}

ERROR RESPONSES:

404 Not Found:
{
    "errors": [{"message": "Task does not exist"}]
}

400 Bad Request:
{
    "errors": [{"message": "Project does not exist"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   API #13: POST /tasks/{task_gid}/addTag/                  ║
║                   Add a tag to a task                                      ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: POST /api/1.0/tasks/{task_gid}/addTag/
Description: Adds a tag to a task.

REQUEST BODY:
{
    "data": {
        "tag": "tag-gid"
    }
}

SUCCESS RESPONSE (200):
{
    "data": {}
}

ERROR RESPONSES:

404 Not Found:
{
    "errors": [{"message": "Task does not exist"}]
}

400 Bad Request:
{
    "errors": [{"message": "Tag does not exist"}]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #14: GET /users/                                ║
║                        Get all users                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/users/
Description: Returns all users in the system.

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "user-gid",
            "resource_type": "user",
            "name": "John Doe",
            "email": "john@example.com"
        }
    ]
}
"""


"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        API #15: GET /projects/                             ║
║                        Get all projects                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

Endpoint: GET /api/1.0/projects/
Description: Returns all projects the user has access to.

SUCCESS RESPONSE (200):
{
    "data": [
        {
            "gid": "project-gid",
            "resource_type": "project",
            "name": "My Project",
            "archived": false
        }
    ]
}
"""


# ============================================================================
#                        SUMMARY TABLE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FINAL 15 APIs FOR EVALUATION                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ #  │ Method │ Endpoint                                │ Description          ║
╠════╪════════╪═════════════════════════════════════════╪══════════════════════╣
║ 1  │ GET    │ /api/1.0/workspaces/                    │ Get all workspaces   ║
║ 2  │ GET    │ /api/1.0/workspaces/{gid}/              │ Get single workspace ║
║ 3  │ GET    │ /api/1.0/tasks/                         │ Get multiple tasks   ║
║ 4  │ POST   │ /api/1.0/tasks/                         │ Create a task        ║
║ 5  │ GET    │ /api/1.0/tasks/{gid}/                   │ Get a task           ║
║ 6  │ PUT    │ /api/1.0/tasks/{gid}/                   │ Update a task        ║
║ 7  │ DELETE │ /api/1.0/tasks/{gid}/                   │ Delete a task        ║
║ 8  │ GET    │ /api/1.0/tasks/{gid}/subtasks/          │ Get subtasks         ║
║ 9  │ POST   │ /api/1.0/tasks/{gid}/subtasks/          │ Create subtask       ║
║ 10 │ POST   │ /api/1.0/tasks/{gid}/setParent/         │ Set task parent      ║
║ 11 │ GET    │ /workspaces/{gid}/tasks/search/         │ Search tasks         ║
║ 12 │ POST   │ /api/1.0/tasks/{gid}/addProject/        │ Add project to task  ║
║ 13 │ POST   │ /api/1.0/tasks/{gid}/addTag/            │ Add tag to task      ║
║ 14 │ GET    │ /api/1.0/users/                         │ Get all users        ║
║ 15 │ GET    │ /api/1.0/projects/                      │ Get all projects     ║
╚════╧════════╧═════════════════════════════════════════╧══════════════════════╝

All APIs follow the Asana API specification with:
- Proper response structure: {"data": {...}}
- Error format: {"errors": [{"message": "..."}]}
- resource_type included in all responses
- Comprehensive edge case handling
""")


if __name__ == "__main__":
    print("\nTo test these APIs, run the server:")
    print("  cd /home/nxtwave/study/scalar_assignment/backend")
    print("  source .venv/bin/activate")
    print("  python manage.py runserver 0.0.0.0:8000")
    print("\nThen use curl or Postman to test the endpoints at http://localhost:8000/api/1.0/")
