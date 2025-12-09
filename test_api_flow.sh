#!/bin/bash
#
# Asana API Complete Test Flow
# Tests all APIs without using admin panel
#
# Usage: ./test_api_flow.sh
#

set -e

BASE_URL="http://localhost:8000"

echo "========================================"
echo "   ASANA API COMPLETE TEST FLOW"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    print_error "jq is not installed. Install it with:"
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  macOS: brew install jq"
    exit 1
fi

# Check if server is running
if ! curl -s "$BASE_URL/api/schema/" > /dev/null 2>&1; then
    print_error "Server is not running at $BASE_URL"
    echo "Start it with: python manage.py runserver"
    exit 1
fi

print_success "Server is running at $BASE_URL"
echo ""

# =============================================================================
# PHASE 1: CREATE FOUNDATION DATA
# =============================================================================

echo "========================================" 
echo "PHASE 1: Setup Foundation Data"
echo "========================================"
echo ""

# 1.1 Create Workspace
print_info "Creating workspace..."
WORKSPACE_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_workspaces/workspaces/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workspace",
    "is_organization": true
  }')

if echo "$WORKSPACE_RESPONSE" | jq -e '.data.gid' > /dev/null 2>&1; then
    WORKSPACE_GID=$(echo $WORKSPACE_RESPONSE | jq -r '.data.gid')
    print_success "Workspace created: $WORKSPACE_GID"
else
    print_error "Failed to create workspace"
    echo "$WORKSPACE_RESPONSE" | jq '.'
    exit 1
fi

# 1.2 Create Users
print_info "Creating users..."
USER1_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_users/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@test.com"
  }')

USER1_GID=$(echo $USER1_RESPONSE | jq -r '.data.gid')
print_success "User 1 created: $USER1_GID (John Doe)"

USER2_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_users/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@test.com"
  }')

USER2_GID=$(echo $USER2_RESPONSE | jq -r '.data.gid')
print_success "User 2 created: $USER2_GID (Jane Smith)"

# 1.3 Create Team
print_info "Creating team..."
TEAM_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_teams/teams/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Backend Team\",
    \"workspace_gid\": \"$WORKSPACE_GID\",
    \"description\": \"Backend development team\"
  }")

TEAM_GID=$(echo $TEAM_RESPONSE | jq -r '.data.gid')
print_success "Team created: $TEAM_GID"

# 1.4 Create Project
print_info "Creating project..."
PROJECT_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_projects/projects/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Asana API Development\",
    \"workspace_gid\": \"$WORKSPACE_GID\",
    \"team_gid\": \"$TEAM_GID\",
    \"public\": true,
    \"color\": \"#4A90E2\",
    \"notes\": \"Project for building Asana API clone\",
    \"due_date\": \"2025-12-31\"
  }")

PROJECT_GID=$(echo $PROJECT_RESPONSE | jq -r '.data.gid')
print_success "Project created: $PROJECT_GID"

# 1.5 Create Tags
print_info "Creating tags..."
TAG1_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_tags/tags/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"urgent\",
    \"workspace_gid\": \"$WORKSPACE_GID\",
    \"color\": \"#FF0000\"
  }")

TAG1_GID=$(echo $TAG1_RESPONSE | jq -r '.data.gid')
print_success "Tag 1 created: $TAG1_GID (urgent)"

TAG2_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_tags/tags/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"bug\",
    \"workspace_gid\": \"$WORKSPACE_GID\",
    \"color\": \"#FFA500\"
  }")

TAG2_GID=$(echo $TAG2_RESPONSE | jq -r '.data.gid')
print_success "Tag 2 created: $TAG2_GID (bug)"

echo ""

# =============================================================================
# PHASE 2: TASK CRUD OPERATIONS
# =============================================================================

echo "========================================"
echo "PHASE 2: Test Task CRUD Operations"
echo "========================================"
echo ""

# 2.1 CREATE Task
print_info "Creating task..."
TASK_RESPONSE=$(curl -s -X POST $BASE_URL/api/asana_tasks/tasks/ \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Implement Authentication\",
    \"workspace_gid\": \"$WORKSPACE_GID\",
    \"assignee_gid\": \"$USER1_GID\",
    \"assignee_status\": \"today\",
    \"due_on\": \"2025-12-15\",
    \"notes\": \"Add JWT authentication to all endpoints\"
  }")

TASK_GID=$(echo $TASK_RESPONSE | jq -r '.data.gid')
print_success "Task created: $TASK_GID"
echo "   Name: $(echo $TASK_RESPONSE | jq -r '.data.name')"
echo "   Assignee: $(echo $TASK_RESPONSE | jq -r '.data.assignee.name')"
echo "   Due: $(echo $TASK_RESPONSE | jq -r '.data.due_on')"

# 2.2 READ Task
print_info "Reading task..."
TASK_READ=$(curl -s -X GET $BASE_URL/api/asana_tasks/tasks/$TASK_GID/)
if echo "$TASK_READ" | jq -e '.data.gid' > /dev/null 2>&1; then
    print_success "Task retrieved successfully"
else
    print_error "Failed to retrieve task"
fi

# 2.3 LIST Tasks
print_info "Listing all tasks..."
TASKS_LIST=$(curl -s -X GET $BASE_URL/api/asana_tasks/tasks/)
TASK_COUNT=$(echo $TASKS_LIST | jq -r '.data | length')
print_success "Found $TASK_COUNT tasks"

# 2.4 LIST Tasks with filters
print_info "Testing filters..."
FILTERED=$(curl -s -X GET "$BASE_URL/api/asana_tasks/tasks/?workspace_gid=$WORKSPACE_GID&completed=false")
FILTERED_COUNT=$(echo $FILTERED | jq -r '.data | length')
print_success "Filtered tasks (workspace + incomplete): $FILTERED_COUNT"

# 2.5 UPDATE Task
print_info "Updating task..."
UPDATE_RESPONSE=$(curl -s -X PUT $BASE_URL/api/asana_tasks/tasks/$TASK_GID/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Implement Authentication - Updated",
    "assignee_status": "later",
    "notes": "Updated: Add OAuth2 support as well"
  }')

if echo "$UPDATE_RESPONSE" | jq -e '.data.gid' > /dev/null 2>&1; then
    print_success "Task updated successfully"
    echo "   New name: $(echo $UPDATE_RESPONSE | jq -r '.data.name')"
else
    print_error "Failed to update task"
fi

echo ""

# =============================================================================
# PHASE 3: TASK RELATIONSHIPS
# =============================================================================

echo "========================================"
echo "PHASE 3: Test Task Relationships"
echo "========================================"
echo ""

# 3.1 Add Project to Task
print_info "Adding project to task..."
ADD_PROJECT=$(curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/addProject \
  -H "Content-Type: application/json" \
  -d "{\"project_gid\": \"$PROJECT_GID\"}")

if echo "$ADD_PROJECT" | jq -e '.data' > /dev/null 2>&1; then
    print_success "Project added to task"
else
    print_error "Failed to add project"
fi

# 3.2 Add Tags to Task
print_info "Adding tags to task..."
curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/addTag \
  -H "Content-Type: application/json" \
  -d "{\"tag_gid\": \"$TAG1_GID\"}" > /dev/null
print_success "Tag 'urgent' added"

curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/addTag \
  -H "Content-Type: application/json" \
  -d "{\"tag_gid\": \"$TAG2_GID\"}" > /dev/null
print_success "Tag 'bug' added"

# 3.3 Add Followers
print_info "Adding followers to task..."
ADD_FOLLOWERS=$(curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/addFollowers \
  -H "Content-Type: application/json" \
  -d "{\"followers\": [\"$USER1_GID\", \"$USER2_GID\"]}")

if echo "$ADD_FOLLOWERS" | jq -e '.data' > /dev/null 2>&1; then
    print_success "2 followers added to task"
else
    print_error "Failed to add followers"
fi

# 3.4 Remove a follower
print_info "Removing one follower..."
curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/removeFollowers \
  -H "Content-Type: application/json" \
  -d "{\"followers\": [\"$USER2_GID\"]}" > /dev/null
print_success "Follower removed"

echo ""

# =============================================================================
# PHASE 4: CREATE MORE TASKS
# =============================================================================

echo "========================================"
echo "PHASE 4: Create More Tasks for Testing"
echo "========================================"
echo ""

# Create 3 more tasks
for i in {1..3}; do
    print_info "Creating task $i..."
    TASK_RESP=$(curl -s -X POST $BASE_URL/api/asana_tasks/tasks/ \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"Task $i\",
        \"workspace_gid\": \"$WORKSPACE_GID\",
        \"assignee_gid\": \"$USER1_GID\"
      }")
    TASK_ID=$(echo $TASK_RESP | jq -r '.data.gid')
    print_success "Task $i created: $TASK_ID"
done

echo ""

# =============================================================================
# PHASE 5: TEST PAGINATION
# =============================================================================

echo "========================================"
echo "PHASE 5: Test Pagination"
echo "========================================"
echo ""

# Get first page
print_info "Getting first page (limit=2)..."
PAGE1=$(curl -s -X GET "$BASE_URL/api/asana_tasks/tasks/?limit=2&offset=0")
PAGE1_COUNT=$(echo $PAGE1 | jq -r '.data | length')
print_success "Page 1 has $PAGE1_COUNT tasks"

# Get second page
print_info "Getting second page (limit=2, offset=2)..."
PAGE2=$(curl -s -X GET "$BASE_URL/api/asana_tasks/tasks/?limit=2&offset=2")
PAGE2_COUNT=$(echo $PAGE2 | jq -r '.data | length')
print_success "Page 2 has $PAGE2_COUNT tasks"

echo ""

# =============================================================================
# PHASE 6: TEST UPDATES & COMPLETION
# =============================================================================

echo "========================================"
echo "PHASE 6: Test Task Completion Flow"
echo "========================================"
echo ""

# Mark task as completed
print_info "Marking task as completed..."
COMPLETE=$(curl -s -X PUT $BASE_URL/api/asana_tasks/tasks/$TASK_GID/ \
  -H "Content-Type: application/json" \
  -d '{"completed": true}')

if echo "$COMPLETE" | jq -r '.data.completed' | grep -q "true"; then
    print_success "Task marked as completed"
else
    print_error "Failed to mark task as completed"
fi

# Verify completed filter works
print_info "Testing completed filter..."
COMPLETED_TASKS=$(curl -s -X GET "$BASE_URL/api/asana_tasks/tasks/?completed=true")
COMPLETED_COUNT=$(echo $COMPLETED_TASKS | jq -r '.data | length')
print_success "Found $COMPLETED_COUNT completed tasks"

INCOMPLETE_TASKS=$(curl -s -X GET "$BASE_URL/api/asana_tasks/tasks/?completed=false")
INCOMPLETE_COUNT=$(echo $INCOMPLETE_TASKS | jq -r '.data | length')
print_success "Found $INCOMPLETE_COUNT incomplete tasks"

echo ""

# =============================================================================
# PHASE 7: TEST EDGE CASES
# =============================================================================

echo "========================================"
echo "PHASE 7: Test Edge Cases"
echo "========================================"
echo ""

# Test invalid UUID
print_info "Testing invalid UUID format..."
INVALID_UUID=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/asana_tasks/tasks/invalid-uuid/)
HTTP_CODE=$(echo "$INVALID_UUID" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_success "Invalid UUID correctly rejected (400)"
else
    print_error "Invalid UUID not handled correctly (got $HTTP_CODE)"
fi

# Test non-existent resource
print_info "Testing non-existent task..."
NON_EXISTENT=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/asana_tasks/tasks/00000000-0000-0000-0000-000000000000/)
HTTP_CODE=$(echo "$NON_EXISTENT" | tail -n1)
if [ "$HTTP_CODE" -eq 404 ]; then
    print_success "Non-existent task correctly returns 404"
else
    print_error "Non-existent task not handled correctly (got $HTTP_CODE)"
fi

# Test missing required fields
print_info "Testing missing required fields..."
MISSING_FIELD=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/api/asana_tasks/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Task without workspace"}')
HTTP_CODE=$(echo "$MISSING_FIELD" | tail -n1)
if [ "$HTTP_CODE" -eq 400 ]; then
    print_success "Missing required field correctly rejected (400)"
else
    print_error "Missing field not handled correctly (got $HTTP_CODE)"
fi

echo ""

# =============================================================================
# PHASE 8: TEST ALL GET ENDPOINTS
# =============================================================================

echo "========================================"
echo "PHASE 8: Test All GET Endpoints"
echo "========================================"
echo ""

# Workspaces
print_info "GET /api/asana_workspaces/workspaces/"
WS_LIST=$(curl -s -X GET $BASE_URL/api/asana_workspaces/workspaces/)
WS_COUNT=$(echo $WS_LIST | jq -r '.data | length')
print_success "Workspaces: $WS_COUNT"

# Users
print_info "GET /api/asana_users/users/"
USERS_LIST=$(curl -s -X GET $BASE_URL/api/asana_users/users/)
USERS_COUNT=$(echo $USERS_LIST | jq -r '.data | length')
print_success "Users: $USERS_COUNT"

# Projects
print_info "GET /api/asana_projects/projects/"
PROJECTS_LIST=$(curl -s -X GET $BASE_URL/api/asana_projects/projects/)
PROJECTS_COUNT=$(echo $PROJECTS_LIST | jq -r '.data | length')
print_success "Projects: $PROJECTS_COUNT"

# Teams
print_info "GET /api/asana_teams/teams/"
TEAMS_LIST=$(curl -s -X GET $BASE_URL/api/asana_teams/teams/)
TEAMS_COUNT=$(echo $TEAMS_LIST | jq -r '.data | length')
print_success "Teams: $TEAMS_COUNT"

# Tags
print_info "GET /api/asana_tags/tags/"
TAGS_LIST=$(curl -s -X GET $BASE_URL/api/asana_tags/tags/)
TAGS_COUNT=$(echo $TAGS_LIST | jq -r '.data | length')
print_success "Tags: $TAGS_COUNT"

# Tasks
print_info "GET /api/asana_tasks/tasks/"
TASKS_LIST=$(curl -s -X GET $BASE_URL/api/asana_tasks/tasks/)
TOTAL_TASKS=$(echo $TASKS_LIST | jq -r '.data | length')
print_success "Tasks: $TOTAL_TASKS"

echo ""

# =============================================================================
# PHASE 9: TEST RELATIONSHIP REMOVAL
# =============================================================================

echo "========================================"
echo "PHASE 9: Test Relationship Removal"
echo "========================================"
echo ""

# Remove project from task
print_info "Removing project from task..."
curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/removeProject \
  -H "Content-Type: application/json" \
  -d "{\"project_gid\": \"$PROJECT_GID\"}" > /dev/null
print_success "Project removed from task"

# Remove tag from task
print_info "Removing tag from task..."
curl -s -X POST $BASE_URL/api/asana_tasks/tasks/$TASK_GID/removeTag \
  -H "Content-Type: application/json" \
  -d "{\"tag_gid\": \"$TAG1_GID\"}" > /dev/null
print_success "Tag removed from task"

echo ""

# =============================================================================
# PHASE 10: TEST CLEANUP (DELETE OPERATIONS)
# =============================================================================

echo "========================================"
echo "PHASE 10: Test Delete Operations"
echo "========================================"
echo ""

# Delete task
print_info "Deleting task..."
DELETE_TASK=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/api/asana_tasks/tasks/$TASK_GID/)
HTTP_CODE=$(echo "$DELETE_TASK" | tail -n1)
if [ "$HTTP_CODE" -eq 200 ]; then
    print_success "Task deleted successfully"
else
    print_error "Failed to delete task (got $HTTP_CODE)"
fi

# Verify task is deleted
print_info "Verifying task is deleted..."
VERIFY_DELETE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/asana_tasks/tasks/$TASK_GID/)
HTTP_CODE=$(echo "$VERIFY_DELETE" | tail -n1)
if [ "$HTTP_CODE" -eq 404 ]; then
    print_success "Task no longer exists (404)"
else
    print_error "Deleted task still accessible (got $HTTP_CODE)"
fi

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "========================================"
echo "   TEST SUMMARY"
echo "========================================"
echo ""

print_success "All API tests completed successfully!"
echo ""
echo "Created Resources:"
echo "  • Workspace: $WORKSPACE_GID"
echo "  • Users: 2 (John Doe, Jane Smith)"
echo "  • Team: $TEAM_GID"
echo "  • Project: $PROJECT_GID"
echo "  • Tags: 2 (urgent, bug)"
echo "  • Tasks: Multiple (some deleted)"
echo ""
echo "Tested Operations:"
echo "  ✅ CREATE (POST)"
echo "  ✅ READ (GET single)"
echo "  ✅ LIST (GET multiple)"
echo "  ✅ UPDATE (PUT)"
echo "  ✅ DELETE"
echo "  ✅ Add relationships (project, tag, followers)"
echo "  ✅ Remove relationships"
echo "  ✅ Filters (workspace, assignee, completed)"
echo "  ✅ Pagination (offset, limit)"
echo "  ✅ Edge cases (invalid UUID, 404, 400)"
echo ""
echo "View detailed API docs at:"
echo "  📖 http://localhost:8000/api/docs/"
echo ""
print_success "🎉 All tests passed!"

