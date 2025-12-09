# Asana API Clone - Final 15 APIs for Evaluation

## 📋 Overview

This project implements the Asana REST API based on the OpenAPI 3.0 specification (`api_spec.txt`). All APIs follow the exact same response structure, error handling, and endpoint patterns as the official Asana API.

**Base URL:** `http://localhost:8000/api/1.0`

---

## 🚀 Quick Start

```bash
# Navigate to project directory
cd /home/nxtwave/study/scalar_assignment/backend

# Activate virtual environment
source .venv/bin/activate

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000
```

---

## 🔐 Response Schemas (Matching Asana API Spec)

### ✅ Success Response
```json
{
    "data": {
        "gid": "12345",
        "resource_type": "project",
        "name": "Project Name",
        ...
    }
}
```

### ❌ Error Response (Exact Asana Format)
```json
{
    "errors": [
        {
            "message": "project: Missing input",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors",
            "phrase": "6 sad squid snuggle softly"
        }
    ]
}
```

| Field | Description |
|-------|-------------|
| `message` | Error description (always present) |
| `help` | URL to documentation (always present) |
| `phrase` | Random phrase (500 errors only) |

---

## 🎯 FINAL 15 APIs FOR EVALUATION

| # | Method | Endpoint | Type | Complexity |
|---|--------|----------|------|------------|
| 1 | `GET` | `/api/1.0/projects/` | List | Basic |
| 2 | `POST` | `/api/1.0/projects/` | Create | Medium |
| 3 | `GET` | `/api/1.0/projects/{project_gid}/` | Read | Basic |
| 4 | `PUT` | `/api/1.0/projects/{project_gid}/` | Update | Medium |
| 5 | `DELETE` | `/api/1.0/projects/{project_gid}/` | Delete | Basic |
| 6 | `POST` | `/api/1.0/projects/{project_gid}/duplicate/` | Action | **Complex** |
| 7 | `GET` | `/api/1.0/projects/{project_gid}/tasks/` | Relationship | Medium |
| 8 | `POST` | `/api/1.0/projects/{project_gid}/addMembers/` | Relationship | **Complex** |
| 9 | `POST` | `/api/1.0/projects/{project_gid}/removeMembers/` | Relationship | Medium |
| 10 | `POST` | `/api/1.0/projects/{project_gid}/addFollowers/` | Relationship | Medium |
| 11 | `POST` | `/api/1.0/projects/{project_gid}/removeFollowers/` | Relationship | Medium |
| 12 | `GET` | `/api/1.0/workspaces/{workspace_gid}/projects/` | Scoped List | Medium |
| 13 | `GET` | `/api/1.0/teams/{team_gid}/projects/` | Scoped List | Medium |
| 14 | `GET` | `/api/1.0/tasks/{task_gid}/subtasks/` | Relationship | **Complex** |
| 15 | `POST` | `/api/1.0/tasks/{task_gid}/setParent/` | Hierarchy | **Complex** |

---

## 📝 Detailed API Documentation

---

### API #1: GET /projects/
**Get multiple projects**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /projects` |
| **Implementation** | `GET /api/1.0/projects/` |

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `workspace` | string | Filter by workspace GID |
| `team` | string | Filter by team GID |
| `archived` | boolean | Filter archived projects |
| `limit` | integer | Results per page (1-100) |
| `offset` | integer | Pagination offset |

**✅ Success (200):**
```json
{
    "data": [
        {
            "gid": "project-uuid",
            "resource_type": "project",
            "name": "My Project",
            "archived": false,
            "color": "light-blue"
        }
    ]
}
```

---

### API #2: POST /projects/
**Create a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects` |
| **Implementation** | `POST /api/1.0/projects/` |

**Request Body:**
```json
{
    "data": {
        "name": "New Project",
        "workspace": "workspace-gid",
        "team": "team-gid",
        "color": "light-blue",
        "default_view": "list",
        "notes": "Project description"
    }
}
```

**✅ Success (201):**
```json
{
    "data": {
        "gid": "new-project-gid",
        "resource_type": "project",
        "name": "New Project",
        "archived": false,
        "workspace": {
            "gid": "ws-gid",
            "resource_type": "workspace",
            "name": "Workspace"
        }
    }
}
```

**❌ Error (400) - Missing field:**
```json
{
    "errors": [
        {
            "message": "name: Missing input",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #3: GET /projects/{project_gid}/
**Get a single project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /projects/{project_gid}` |
| **Implementation** | `GET /api/1.0/projects/{project_gid}/` |

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Project Name",
        "archived": false,
        "color": "light-green",
        "completed": false,
        "created_at": "2025-12-09T10:00:00Z",
        "modified_at": "2025-12-09T10:00:00Z",
        "workspace": {"gid": "...", "resource_type": "workspace", "name": "..."},
        "team": {"gid": "...", "resource_type": "team", "name": "..."}
    }
}
```

**❌ Error (404):**
```json
{
    "errors": [
        {
            "message": "project: Unknown object: invalid-gid",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #4: PUT /projects/{project_gid}/
**Update a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `PUT /projects/{project_gid}` |
| **Implementation** | `PUT /api/1.0/projects/{project_gid}/` |

**Request Body:**
```json
{
    "data": {
        "name": "Updated Name",
        "archived": true,
        "color": "dark-blue"
    }
}
```

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Updated Name",
        "archived": true
    }
}
```

**❌ Error (400) - Read-only field:**
```json
{
    "errors": [
        {
            "message": "workspace: Cannot modify read-only field",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #5: DELETE /projects/{project_gid}/
**Delete a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `DELETE /projects/{project_gid}` |
| **Implementation** | `DELETE /api/1.0/projects/{project_gid}/` |

**✅ Success (200):**
```json
{
    "data": {}
}
```

---

### API #6: POST /projects/{project_gid}/duplicate/ (COMPLEX)
**Duplicate a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects/{project_gid}/duplicate` |
| **Implementation** | `POST /api/1.0/projects/{project_gid}/duplicate/` |

**Request Body:**
```json
{
    "data": {
        "name": "Copy of Project",
        "include": ["members", "notes", "task_notes"]
    }
}
```

**✅ Success (201):**
```json
{
    "data": {
        "gid": "job-gid",
        "resource_type": "job",
        "resource_subtype": "duplicate_project",
        "status": "succeeded",
        "new_project": {
            "gid": "new-project-gid",
            "resource_type": "project",
            "name": "Copy of Project"
        }
    }
}
```

---

### API #7: GET /projects/{project_gid}/tasks/
**Get tasks for a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /projects/{project_gid}/tasks` |
| **Implementation** | `GET /api/1.0/projects/{project_gid}/tasks/` |

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `limit` | integer | Results per page (1-100) |
| `offset` | integer | Pagination offset |

**✅ Success (200):**
```json
{
    "data": [
        {
            "gid": "task-gid",
            "resource_type": "task",
            "name": "Task 1",
            "completed": false
        }
    ]
}
```

---

### API #8: POST /projects/{project_gid}/addMembers/ (COMPLEX)
**Add members to a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects/{project_gid}/addMembers` |
| **Implementation** | `POST /api/1.0/projects/{project_gid}/addMembers/` |

**Request Body:**
```json
{
    "data": {
        "members": "user-gid-1,user-gid-2"
    }
}
```

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Project Name",
        "members": [
            {"gid": "user-1", "resource_type": "user", "name": "User 1"},
            {"gid": "user-2", "resource_type": "user", "name": "User 2"}
        ]
    }
}
```

**❌ Error (404) - User not found:**
```json
{
    "errors": [
        {
            "message": "user: Unknown object: invalid-user-gid",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #9: POST /projects/{project_gid}/removeMembers/
**Remove members from a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects/{project_gid}/removeMembers` |
| **Implementation** | `POST /api/1.0/projects/{project_gid}/removeMembers/` |

**Request Body:**
```json
{
    "data": {
        "members": "user-gid-1,user-gid-2"
    }
}
```

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Project Name"
    }
}
```

---

### API #10: POST /projects/{project_gid}/addFollowers/
**Add followers to a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects/{project_gid}/addFollowers` |
| **Implementation** | `POST /api/1.0/projects/{project_gid}/addFollowers/` |

**Request Body:**
```json
{
    "data": {
        "followers": "user-gid-1,user-gid-2"
    }
}
```

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Project Name",
        "followers": [
            {"gid": "user-1", "resource_type": "user", "name": "User 1"}
        ]
    }
}
```

---

### API #11: POST /projects/{project_gid}/removeFollowers/
**Remove followers from a project**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /projects/{project_gid}/removeFollowers` |
| **Implementation** | `POST /api/1.0/projects/{project_gid}/removeFollowers/` |

**Request Body:**
```json
{
    "data": {
        "followers": "user-gid-1"
    }
}
```

**✅ Success (200):**
```json
{
    "data": {
        "gid": "project-gid",
        "resource_type": "project",
        "name": "Project Name"
    }
}
```

---

### API #12: GET /workspaces/{workspace_gid}/projects/
**Get projects in a workspace**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /workspaces/{workspace_gid}/projects` |
| **Implementation** | `GET /api/1.0/workspaces/{workspace_gid}/projects/` |

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `archived` | boolean | Filter by archived status |
| `limit` | integer | Results per page (1-100) |
| `offset` | integer | Pagination offset |

**✅ Success (200):**
```json
{
    "data": [
        {
            "gid": "project-gid",
            "resource_type": "project",
            "name": "Project 1",
            "archived": false
        }
    ]
}
```

---

### API #13: GET /teams/{team_gid}/projects/
**Get projects in a team**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /teams/{team_gid}/projects` |
| **Implementation** | `GET /api/1.0/teams/{team_gid}/projects/` |

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `archived` | boolean | Filter by archived status |
| `limit` | integer | Results per page (1-100) |

**✅ Success (200):**
```json
{
    "data": [
        {
            "gid": "project-gid",
            "resource_type": "project",
            "name": "Team Project",
            "archived": false,
            "color": "light-green"
        }
    ]
}
```

**❌ Error (404) - Team not found:**
```json
{
    "errors": [
        {
            "message": "team: Unknown object: invalid-gid",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #14: GET /tasks/{task_gid}/subtasks/ (COMPLEX)
**Get subtasks from a task**

| Property | Value |
|----------|-------|
| **Asana Spec** | `GET /tasks/{task_gid}/subtasks` |
| **Implementation** | `GET /api/1.0/tasks/{task_gid}/subtasks/` |

**✅ Success (200):**
```json
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
```

**❌ Error (400) - Invalid GID:**
```json
{
    "errors": [
        {
            "message": "task_gid: Invalid GID format",
            "help": "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"
        }
    ]
}
```

---

### API #15: POST /tasks/{task_gid}/setParent/ (COMPLEX)
**Set the parent of a task (hierarchy management)**

| Property | Value |
|----------|-------|
| **Asana Spec** | `POST /tasks/{task_gid}/setParent` |
| **Implementation** | `POST /api/1.0/tasks/{task_gid}/setParent/` |

**Request Body:**
```json
{
    "data": {
        "parent": "parent-task-gid"
    }
}
```

**✅ Success (200):**
```json
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
```

**Edge Cases Handled:**

| Scenario | Error Message |
|----------|--------------|
| Self-reference | `parent: Cannot set a task as its own parent` |
| Circular hierarchy | `parent: Cannot create circular reference in task hierarchy` |
| Different workspace | `parent: Parent task must be in the same workspace` |

---

## 🧪 Test Commands

```bash
# 1. Get all projects
curl http://localhost:8000/api/1.0/projects/

# 2. Create a project
curl -X POST http://localhost:8000/api/1.0/projects/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Test Project", "workspace": "WORKSPACE_GID"}}'

# 3. Get a project
curl http://localhost:8000/api/1.0/projects/{project_gid}/

# 4. Update a project
curl -X PUT http://localhost:8000/api/1.0/projects/{project_gid}/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Updated Name"}}'

# 5. Delete a project
curl -X DELETE http://localhost:8000/api/1.0/projects/{project_gid}/

# 6. Duplicate a project
curl -X POST http://localhost:8000/api/1.0/projects/{project_gid}/duplicate/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "Copy of Project"}}'

# 7. Get project tasks
curl http://localhost:8000/api/1.0/projects/{project_gid}/tasks/

# 8. Add members to project
curl -X POST http://localhost:8000/api/1.0/projects/{project_gid}/addMembers/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"members": "USER_GID"}}'

# 9. Remove members from project
curl -X POST http://localhost:8000/api/1.0/projects/{project_gid}/removeMembers/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"members": "USER_GID"}}'

# 10. Add followers
curl -X POST http://localhost:8000/api/1.0/projects/{project_gid}/addFollowers/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"followers": "USER_GID"}}'

# 11. Remove followers
curl -X POST http://localhost:8000/api/1.0/projects/{project_gid}/removeFollowers/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"followers": "USER_GID"}}'

# 12. Get workspace projects
curl http://localhost:8000/api/1.0/workspaces/{workspace_gid}/projects/

# 13. Get team projects
curl http://localhost:8000/api/1.0/teams/{team_gid}/projects/

# 14. Get subtasks
curl http://localhost:8000/api/1.0/tasks/{task_gid}/subtasks/

# 15. Set parent (make subtask)
curl -X POST http://localhost:8000/api/1.0/tasks/{task_gid}/setParent/ \
  -H "Content-Type: application/json" \
  -d '{"data": {"parent": "PARENT_TASK_GID"}}'

# Test error responses
curl http://localhost:8000/api/1.0/projects/invalid-gid/
curl http://localhost:8000/api/1.0/tasks/invalid-gid/subtasks/
```

---

## 📚 API Documentation

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/
- **API Spec Download:** http://localhost:8000/api/spec/
- **API Info (all endpoints):** http://localhost:8000/api/info/

### API Info Endpoint
```bash
# Get all available endpoints
curl http://localhost:8000/api/info/

# Download original API spec
curl http://localhost:8000/api/spec/ -o api_spec.txt
```

---

## ✅ Implementation Checklist

- [x] All 15 APIs implemented
- [x] Error schema matches Asana API spec (message, help, phrase)
- [x] All responses include `resource_type`
- [x] Proper HTTP status codes (200, 201, 400, 404, 500)
- [x] Rate limiting (5 req/sec)
- [x] Pagination support
- [x] Relationship operations (members, followers)
- [x] Complex hierarchy operations (subtasks, setParent)
- [x] Circular reference prevention
- [x] Read-only field validation

---

## 📄 License

This project is for educational/assignment purposes.
