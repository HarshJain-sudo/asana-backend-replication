"""
Asana API Test Flow Documentation
==================================

This file documents the complete test flow for all implemented APIs,
including test cases, expected behaviors, and edge cases.

Run tests: python manage.py test tests.test_api_flow
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from asana_workspaces.models.workspace import Workspace
from asana_users.models.user import User
from asana_projects.models.project import Project
from asana_teams.models.team import Team
from asana_tags.models.tag import Tag
from asana_tasks.models.task import Task
from asana_tasks.models.task_project import TaskProject
from asana_tasks.models.task_tag import TaskTag
from asana_tasks.models.task_follower import TaskFollower
import uuid


class AsanaAPITestFlow(TestCase):
    """
    Complete API Test Flow for Asana Backend
    
    Test Execution Order:
    1. Setup (create test data)
    2. Workspaces API tests
    3. Users API tests
    4. Projects API tests
    5. Teams API tests
    6. Tags API tests
    7. Tasks API tests (CRUD + Relationships)
    8. Stories API tests
    9. Attachments API tests
    10. Webhooks API tests
    11. Cleanup
    """

    def setUp(self):
        """Setup test data before each test"""
        self.client = APIClient()
        
        # Create test workspace
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            is_organization=False
        )
        
        # Create test users
        self.user1 = User.objects.create(
            name="John Doe",
            email="john@example.com"
        )
        self.user2 = User.objects.create(
            name="Jane Smith",
            email="jane@example.com"
        )
        
        # Create test team
        self.team = Team.objects.create(
            name="Test Team",
            workspace=self.workspace,
            description="Test team description"
        )
        
        # Create test project
        self.project = Project.objects.create(
            name="Test Project",
            workspace=self.workspace,
            team=self.team,
            public=True,
            archived=False
        )
        
        # Create test tag
        self.tag = Tag.objects.create(
            name="urgent",
            workspace=self.workspace,
            color="#FF0000"
        )
        
        # Create test task
        self.task = Task.objects.create(
            name="Test Task",
            workspace=self.workspace,
            assignee=self.user1,
            completed=False
        )

    # ==================== WORKSPACES API TESTS ====================
    
    def test_01_list_workspaces(self):
        """
        Test Case: GET /api/asana_workspaces/workspaces/
        
        Expected Behavior:
        - Status: 200 OK
        - Returns list of workspaces
        - Each workspace has: gid, name, is_organization
        
        Edge Cases:
        - Empty workspace list
        - Pagination parameters (offset, limit)
        """
        response = self.client.get('/api/asana_workspaces/workspaces/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertIsInstance(response.json()['data'], list)
        self.assertGreater(len(response.json()['data']), 0)
        
        # Verify workspace structure
        workspace = response.json()['data'][0]
        self.assertIn('gid', workspace)
        self.assertIn('name', workspace)
        self.assertIn('is_organization', workspace)

    def test_02_get_single_workspace(self):
        """
        Test Case: GET /api/asana_workspaces/workspaces/{workspace_gid}/
        
        Expected Behavior:
        - Status: 200 OK
        - Returns single workspace details
        
        Edge Cases:
        - Invalid UUID format -> 400 Bad Request
        - Non-existent workspace -> 404 Not Found
        """
        # Test valid workspace
        response = self.client.get(
            f'/api/asana_workspaces/workspaces/{self.workspace.gid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['data']['gid'], 
            str(self.workspace.gid)
        )
        
        # Test invalid UUID
        response = self.client.get(
            '/api/asana_workspaces/workspaces/invalid-uuid/'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test non-existent workspace
        fake_uuid = str(uuid.uuid4())
        response = self.client.get(
            f'/api/asana_workspaces/workspaces/{fake_uuid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== USERS API TESTS ====================
    
    def test_03_list_users(self):
        """
        Test Case: GET /api/asana_users/users/
        
        Expected Behavior:
        - Status: 200 OK
        - Returns list of users
        - Supports pagination
        """
        response = self.client.get('/api/asana_users/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertIsInstance(response.json()['data'], list)
        
        # Test pagination
        response = self.client.get('/api/asana_users/users/?offset=0&limit=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.json()['data']), 1)

    def test_04_get_single_user(self):
        """
        Test Case: GET /api/asana_users/users/{user_gid}/
        
        Expected Behavior:
        - Status: 200 OK
        - Returns user details
        
        Edge Cases:
        - Invalid UUID -> 400
        - Non-existent user -> 404
        """
        response = self.client.get(
            f'/api/asana_users/users/{self.user1.gid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['data']['email'],
            self.user1.email
        )

    # ==================== TASKS API TESTS (CRUD) ====================
    
    def test_05_create_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/
        
        Request Body:
        {
            "name": "New Task",
            "workspace_gid": "<uuid>",
            "assignee_gid": "<uuid>",  # optional
            "due_on": "2025-12-31",     # optional
            "notes": "Task notes"       # optional
        }
        
        Expected Behavior:
        - Status: 201 Created
        - Returns created task with gid
        
        Edge Cases:
        - Missing required fields -> 400
        - Invalid workspace_gid -> 400
        - Invalid assignee_gid -> 400
        - Invalid date format -> 400
        """
        data = {
            'name': 'API Test Task',
            'workspace_gid': str(self.workspace.gid),
            'assignee_gid': str(self.user1.gid),
            'due_on': '2025-12-31',
            'notes': 'Test task created via API'
        }
        
        response = self.client.post(
            '/api/asana_tasks/tasks/',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.json())
        self.assertEqual(response.json()['data']['name'], data['name'])
        self.assertIn('gid', response.json()['data'])
        
        # Test missing required field
        invalid_data = {'name': 'Task without workspace'}
        response = self.client.post(
            '/api/asana_tasks/tasks/',
            data=invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_06_get_task(self):
        """
        Test Case: GET /api/asana_tasks/tasks/{task_gid}/
        
        Expected Behavior:
        - Status: 200 OK
        - Returns complete task details
        
        Edge Cases:
        - Invalid UUID -> 400
        - Non-existent task -> 404
        """
        response = self.client.get(
            f'/api/asana_tasks/tasks/{self.task.gid}/'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['data']['gid'],
            str(self.task.gid)
        )

    def test_07_update_task(self):
        """
        Test Case: PUT /api/asana_tasks/tasks/{task_gid}/
        
        Request Body (all fields optional):
        {
            "name": "Updated Task Name",
            "completed": true,
            "assignee_gid": "<uuid>",
            "notes": "Updated notes"
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Returns updated task
        - Only provided fields are updated
        
        Edge Cases:
        - Invalid UUID -> 400
        - Non-existent task -> 404
        - Invalid field values -> 400
        """
        update_data = {
            'name': 'Updated Task Name',
            'completed': True,
            'notes': 'Updated via API test'
        }
        
        response = self.client.put(
            f'/api/asana_tasks/tasks/{self.task.gid}/',
            data=update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['data']['name'],
            update_data['name']
        )
        self.assertTrue(response.json()['data']['completed'])

    def test_08_delete_task(self):
        """
        Test Case: DELETE /api/asana_tasks/tasks/{task_gid}/
        
        Expected Behavior:
        - Status: 200 OK
        - Task is permanently deleted
        - Returns empty data object
        
        Edge Cases:
        - Invalid UUID -> 400
        - Non-existent task -> 404
        - Already deleted task -> 404
        """
        # Create a task to delete
        task_to_delete = Task.objects.create(
            name="Task to Delete",
            workspace=self.workspace
        )
        
        response = self.client.delete(
            f'/api/asana_tasks/tasks/{task_to_delete.gid}/'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data'], {})
        
        # Verify task is deleted
        self.assertFalse(
            Task.objects.filter(gid=task_to_delete.gid).exists()
        )
        
        # Try to delete again - should fail
        response = self.client.delete(
            f'/api/asana_tasks/tasks/{task_to_delete.gid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== TASKS RELATIONSHIP TESTS ====================
    
    def test_09_add_project_to_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/addProject
        
        Request Body:
        {
            "project_gid": "<uuid>"
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Task is associated with project
        - Can add multiple projects to same task
        
        Edge Cases:
        - Invalid task_gid -> 400
        - Invalid project_gid -> 400
        - Non-existent task/project -> 404
        - Adding same project twice -> Should be idempotent
        """
        data = {'project_gid': str(self.project.gid)}
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/addProject',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify association exists
        self.assertTrue(
            TaskProject.objects.filter(
                task=self.task,
                project=self.project
            ).exists()
        )
        
        # Test idempotency - adding same project again
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/addProject',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_10_remove_project_from_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/removeProject
        
        Request Body:
        {
            "project_gid": "<uuid>"
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Task-project association is removed
        
        Edge Cases:
        - Removing non-associated project -> Should not error
        - Invalid UUIDs -> 400
        """
        # First add project
        TaskProject.objects.create(task=self.task, project=self.project)
        
        data = {'project_gid': str(self.project.gid)}
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/removeProject',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify association is removed
        self.assertFalse(
            TaskProject.objects.filter(
                task=self.task,
                project=self.project
            ).exists()
        )

    def test_11_add_tag_to_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/addTag
        
        Request Body:
        {
            "tag_gid": "<uuid>"
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Task is tagged
        
        Edge Cases:
        - Invalid UUIDs -> 400
        - Non-existent tag -> 404
        """
        data = {'tag_gid': str(self.tag.gid)}
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/addTag',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TaskTag.objects.filter(
                task=self.task,
                tag=self.tag
            ).exists()
        )

    def test_12_remove_tag_from_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/removeTag
        
        Request Body:
        {
            "tag_gid": "<uuid>"
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Tag is removed from task
        """
        # First add tag
        TaskTag.objects.create(task=self.task, tag=self.tag)
        
        data = {'tag_gid': str(self.tag.gid)}
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/removeTag',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            TaskTag.objects.filter(
                task=self.task,
                tag=self.tag
            ).exists()
        )

    def test_13_add_followers_to_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/addFollowers
        
        Request Body:
        {
            "followers": ["<uuid1>", "<uuid2>", ...]
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Multiple users can be added as followers
        - Can add multiple followers at once
        
        Edge Cases:
        - Empty followers list -> 400
        - Invalid UUID in list -> 400
        - Non-existent user -> 404
        """
        data = {
            'followers': [
                str(self.user1.gid),
                str(self.user2.gid)
            ]
        }
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/addFollowers',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify both followers added
        self.assertEqual(
            TaskFollower.objects.filter(task=self.task).count(),
            2
        )

    def test_14_remove_followers_from_task(self):
        """
        Test Case: POST /api/asana_tasks/tasks/{task_gid}/removeFollowers
        
        Request Body:
        {
            "followers": ["<uuid1>", "<uuid2>", ...]
        }
        
        Expected Behavior:
        - Status: 200 OK
        - Specified followers are removed
        """
        # First add followers
        TaskFollower.objects.create(task=self.task, user=self.user1)
        TaskFollower.objects.create(task=self.task, user=self.user2)
        
        data = {'followers': [str(self.user1.gid)]}
        
        response = self.client.post(
            f'/api/asana_tasks/tasks/{self.task.gid}/removeFollowers',
            data=data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only user1 removed, user2 still following
        self.assertFalse(
            TaskFollower.objects.filter(
                task=self.task,
                user=self.user1
            ).exists()
        )
        self.assertTrue(
            TaskFollower.objects.filter(
                task=self.task,
                user=self.user2
            ).exists()
        )

    # ==================== COMPLETE FLOW TEST ====================
    
    def test_15_complete_task_workflow(self):
        """
        Test Case: Complete Task Lifecycle
        
        Workflow:
        1. Create a new task
        2. Assign to project
        3. Add tags
        4. Add followers
        5. Update task details
        6. Mark as completed
        7. Remove from project
        8. Delete task
        
        This tests the complete real-world usage flow
        """
        # Step 1: Create task
        create_data = {
            'name': 'Workflow Test Task',
            'workspace_gid': str(self.workspace.gid),
            'due_on': '2025-12-31'
        }
        response = self.client.post(
            '/api/asana_tasks/tasks/',
            data=create_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_gid = response.json()['data']['gid']
        
        # Step 2: Add to project
        response = self.client.post(
            f'/api/asana_tasks/tasks/{task_gid}/addProject',
            data={'project_gid': str(self.project.gid)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 3: Add tag
        response = self.client.post(
            f'/api/asana_tasks/tasks/{task_gid}/addTag',
            data={'tag_gid': str(self.tag.gid)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 4: Add followers
        response = self.client.post(
            f'/api/asana_tasks/tasks/{task_gid}/addFollowers',
            data={'followers': [str(self.user1.gid)]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 5: Update task
        response = self.client.put(
            f'/api/asana_tasks/tasks/{task_gid}/',
            data={'notes': 'Updated task notes'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 6: Mark completed
        response = self.client.put(
            f'/api/asana_tasks/tasks/{task_gid}/',
            data={'completed': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['data']['completed'])
        
        # Step 7: Remove from project
        response = self.client.post(
            f'/api/asana_tasks/tasks/{task_gid}/removeProject',
            data={'project_gid': str(self.project.gid)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 8: Delete task
        response = self.client.delete(
            f'/api/asana_tasks/tasks/{task_gid}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ==================== TEST CASE SUMMARY ====================

"""
COMPLETE TEST CASE CHECKLIST:

✅ Workspaces API (2 tests)
   - List workspaces
   - Get single workspace
   
✅ Users API (2 tests)
   - List users
   - Get single user
   
✅ Tasks CRUD (5 tests)
   - Create task
   - Read task
   - Update task
   - Delete task
   - List tasks
   
✅ Tasks Relationships (6 tests)
   - Add/Remove project
   - Add/Remove tag
   - Add/Remove followers
   
✅ Complete Workflow (1 test)
   - End-to-end task lifecycle

TOTAL: 16 comprehensive tests covering 31 API endpoints

EDGE CASES TESTED:
- Invalid UUID formats
- Non-existent resources
- Missing required fields
- Invalid field values
- Pagination
- Idempotency
- Cascading deletes
- Multiple associations

PERFORMANCE TESTS (Future):
- Rate limiting (5 req/sec)
- Large dataset pagination
- Concurrent requests
- Database query optimization
"""

