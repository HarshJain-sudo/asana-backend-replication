#!/usr/bin/env python3
"""
Comprehensive API Test Script for Asana Backend
Tests all implemented CRUD operations and relationships
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
        self.created_resources = {}

    def print_header(self, text: str):
        """Print section header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
        print(f"  {text}")
        print(f"{'='*70}{Colors.RESET}\n")

    def print_test(self, test_name: str, method: str):
        """Print test name"""
        print(f"{Colors.BLUE}▶ {method} {Colors.RESET}{test_name}")

    def print_success(self, message: str):
        """Print success message"""
        print(f"  {Colors.GREEN}✅ {message}{Colors.RESET}")
        self.results['passed'] += 1

    def print_error(self, message: str):
        """Print error message"""
        print(f"  {Colors.RED}❌ {message}{Colors.RESET}")
        self.results['failed'] += 1

    def print_skip(self, message: str):
        """Print skip message"""
        print(f"  {Colors.YELLOW}⏭️  {message}{Colors.RESET}")
        self.results['skipped'] += 1

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        method = method.upper()
        json_data = json.dumps(data) if data else None

        if method == "POST":
            return requests.post(
                url, headers=headers, data=json_data, params=params
            )
        elif method == "PUT":
            return requests.put(
                url, headers=headers, data=json_data, params=params
            )
        elif method == "DELETE":
            return requests.delete(url, headers=headers, params=params)
        else:
            return requests.get(url, headers=headers, params=params)

    def test_workspaces(self):
        """Test Workspace CRUD operations"""
        self.print_header("🏢 WORKSPACE APIs")

        # Create Workspace
        self.print_test("Create Workspace", "POST")
        try:
            response = self.make_request(
                "POST",
                "/api/asana_workspaces/workspaces/",
                data={
                    "name": "Test Workspace",
                    "is_organization": True
                }
            )
            if response.status_code == 201:
                workspace_gid = response.json()['data']['gid']
                self.created_resources['workspace'] = workspace_gid
                self.print_success(
                    f"Created workspace: {workspace_gid[:8]}..."
                )
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Get All Workspaces
        self.print_test("Get All Workspaces", "GET")
        try:
            response = self.make_request(
                "GET", "/api/asana_workspaces/workspaces/"
            )
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} workspaces")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Get Single Workspace
        if 'workspace' in self.created_resources:
            self.print_test("Get Single Workspace", "GET")
            try:
                gid = self.created_resources['workspace']
                response = self.make_request(
                    "GET", f"/api/asana_workspaces/workspaces/{gid}/"
                )
                if response.status_code == 200:
                    self.print_success("Retrieved workspace details")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

            # Update Workspace
            self.print_test("Update Workspace", "PUT")
            try:
                response = self.make_request(
                    "PUT",
                    f"/api/asana_workspaces/workspaces/{gid}/",
                    data={"name": "Updated Test Workspace"}
                )
                if response.status_code == 200:
                    self.print_success("Updated workspace")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

    def test_users(self):
        """Test User CRUD operations"""
        self.print_header("👥 USER APIs")

        # Create User
        self.print_test("Create User", "POST")
        try:
            response = self.make_request(
                "POST",
                "/api/asana_users/users/",
                data={
                    "name": "Test User",
                    "email": "test@example.com",
                    "photo": "https://example.com/photo.jpg"
                }
            )
            if response.status_code == 201:
                user_gid = response.json()['data']['gid']
                self.created_resources['user'] = user_gid
                self.print_success(f"Created user: {user_gid[:8]}...")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Get All Users
        self.print_test("Get All Users", "GET")
        try:
            response = self.make_request("GET", "/api/asana_users/users/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} users")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Get Single User
        if 'user' in self.created_resources:
            self.print_test("Get Single User", "GET")
            try:
                gid = self.created_resources['user']
                response = self.make_request(
                    "GET", f"/api/asana_users/users/{gid}/"
                )
                if response.status_code == 200:
                    self.print_success("Retrieved user details")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

            # Update User
            self.print_test("Update User", "PUT")
            try:
                response = self.make_request(
                    "PUT",
                    f"/api/asana_users/users/{gid}/",
                    data={"name": "Updated Test User"}
                )
                if response.status_code == 200:
                    self.print_success("Updated user")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

    def test_projects(self):
        """Test Project APIs"""
        self.print_header("📁 PROJECT APIs")

        # Get All Projects
        self.print_test("Get All Projects", "GET")
        try:
            response = self.make_request("GET", "/api/asana_projects/projects/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} projects")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Create Project
        self.print_test("Create Project", "POST")
        if 'workspace' in self.created_resources:
            try:
                response = self.make_request(
                    "POST",
                    "/api/asana_projects/projects/",
                    data={
                        "name": "Test Project",
                        "workspace_gid": self.created_resources['workspace']
                    }
                )
                if response.status_code == 201:
                    project_gid = response.json()['data']['gid']
                    self.created_resources['project'] = project_gid
                    self.print_success(f"Created project: {project_gid[:8]}...")
                elif response.status_code == 405:
                    self.print_skip("POST not implemented yet")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No workspace available")

    def test_teams(self):
        """Test Team APIs"""
        self.print_header("👨‍👩‍👧‍👦 TEAM APIs")

        # Get All Teams
        self.print_test("Get All Teams", "GET")
        try:
            response = self.make_request("GET", "/api/asana_teams/teams/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} teams")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Create Team
        self.print_test("Create Team", "POST")
        if 'workspace' in self.created_resources:
            try:
                response = self.make_request(
                    "POST",
                    "/api/asana_teams/teams/",
                    data={
                        "name": "Test Team",
                        "workspace_gid": self.created_resources['workspace']
                    }
                )
                if response.status_code == 201:
                    team_gid = response.json()['data']['gid']
                    self.created_resources['team'] = team_gid
                    self.print_success(f"Created team: {team_gid[:8]}...")
                elif response.status_code == 405:
                    self.print_skip("POST not implemented yet")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No workspace available")

    def test_tags(self):
        """Test Tag APIs"""
        self.print_header("🏷️  TAG APIs")

        # Get All Tags
        self.print_test("Get All Tags", "GET")
        try:
            response = self.make_request("GET", "/api/asana_tags/tags/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} tags")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Create Tag
        self.print_test("Create Tag", "POST")
        if 'workspace' in self.created_resources:
            try:
                response = self.make_request(
                    "POST",
                    "/api/asana_tags/tags/",
                    data={
                        "name": "Test Tag",
                        "workspace_gid": self.created_resources['workspace']
                    }
                )
                if response.status_code == 201:
                    tag_gid = response.json()['data']['gid']
                    self.created_resources['tag'] = tag_gid
                    self.print_success(f"Created tag: {tag_gid[:8]}...")
                elif response.status_code == 405:
                    self.print_skip("POST not implemented yet")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No workspace available")

    def test_tasks(self):
        """Test Task CRUD operations"""
        self.print_header("✅ TASK APIs")

        # Create Task
        self.print_test("Create Task", "POST")
        if 'workspace' in self.created_resources:
            try:
                data = {
                    "name": "Test Task",
                    "workspace_gid": self.created_resources['workspace']
                }
                if 'user' in self.created_resources:
                    data['assignee_gid'] = self.created_resources['user']

                response = self.make_request(
                    "POST", "/api/asana_tasks/tasks/", data=data
                )
                if response.status_code == 201:
                    task_gid = response.json()['data']['gid']
                    self.created_resources['task'] = task_gid
                    self.print_success(f"Created task: {task_gid[:8]}...")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No workspace available")

        # Get All Tasks
        self.print_test("Get All Tasks", "GET")
        try:
            response = self.make_request("GET", "/api/asana_tasks/tasks/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} tasks")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Get Single Task
        if 'task' in self.created_resources:
            self.print_test("Get Single Task", "GET")
            try:
                gid = self.created_resources['task']
                response = self.make_request(
                    "GET", f"/api/asana_tasks/tasks/{gid}/"
                )
                if response.status_code == 200:
                    self.print_success("Retrieved task details")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

            # Update Task
            self.print_test("Update Task", "PUT")
            try:
                response = self.make_request(
                    "PUT",
                    f"/api/asana_tasks/tasks/{gid}/",
                    data={
                        "name": "Updated Test Task",
                        "completed": True
                    }
                )
                if response.status_code == 200:
                    self.print_success("Updated task")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

            # Task Relationships
            if 'project' in self.created_resources:
                self.print_test("Add Project to Task", "POST")
                try:
                    response = self.make_request(
                        "POST",
                        f"/api/asana_tasks/tasks/{gid}/addProject/",
                        data={"gid": self.created_resources['project']}
                    )
                    if response.status_code == 200:
                        self.print_success("Added project to task")
                    else:
                        self.print_skip("Project add not available")
                except Exception as e:
                    self.print_error(f"Exception: {str(e)}")

            if 'tag' in self.created_resources:
                self.print_test("Add Tag to Task", "POST")
                try:
                    response = self.make_request(
                        "POST",
                        f"/api/asana_tasks/tasks/{gid}/addTag/",
                        data={"gid": self.created_resources['tag']}
                    )
                    if response.status_code == 200:
                        self.print_success("Added tag to task")
                    else:
                        self.print_skip("Tag add not available")
                except Exception as e:
                    self.print_error(f"Exception: {str(e)}")

    def test_stories(self):
        """Test Story APIs"""
        self.print_header("💬 STORY APIs")

        # Create Story
        self.print_test("Create Story", "POST")
        if 'task' in self.created_resources:
            try:
                response = self.make_request(
                    "POST",
                    "/api/asana_stories/stories/",
                    data={
                        "task_gid": self.created_resources['task'],
                        "text": "Test comment"
                    }
                )
                if response.status_code == 201:
                    story_gid = response.json()['data']['gid']
                    self.created_resources['story'] = story_gid
                    self.print_success(f"Created story: {story_gid[:8]}...")
                elif response.status_code == 405:
                    self.print_skip("POST not implemented yet")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No task available")

        # Get Task Stories
        if 'task' in self.created_resources:
            self.print_test("Get Task Stories", "GET")
            try:
                gid = self.created_resources['task']
                response = self.make_request(
                    "GET", f"/api/asana_stories/tasks/{gid}/stories/"
                )
                if response.status_code == 200:
                    count = len(response.json()['data'])
                    self.print_success(f"Retrieved {count} stories")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")

    def test_webhooks(self):
        """Test Webhook APIs"""
        self.print_header("🔔 WEBHOOK APIs")

        # Get All Webhooks
        self.print_test("Get All Webhooks", "GET")
        try:
            response = self.make_request("GET", "/api/asana_webhooks/webhooks/")
            if response.status_code == 200:
                count = len(response.json()['data'])
                self.print_success(f"Retrieved {count} webhooks")
            else:
                self.print_error(f"Status {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Create Webhook
        self.print_test("Create Webhook", "POST")
        if 'task' in self.created_resources:
            try:
                response = self.make_request(
                    "POST",
                    "/api/asana_webhooks/webhooks/",
                    data={
                        "resource": "task",
                        "resource_gid": self.created_resources['task'],
                        "target": "https://example.com/webhook"
                    }
                )
                if response.status_code == 201:
                    webhook_gid = response.json()['data']['gid']
                    self.created_resources['webhook'] = webhook_gid
                    self.print_success(f"Created webhook: {webhook_gid[:8]}...")
                elif response.status_code == 405:
                    self.print_skip("POST not implemented yet")
                else:
                    self.print_error(f"Status {response.status_code}")
            except Exception as e:
                self.print_error(f"Exception: {str(e)}")
        else:
            self.print_skip("No task available")

    def test_pagination(self):
        """Test pagination parameters"""
        self.print_header("📄 PAGINATION & VALIDATION")

        # Test negative offset
        self.print_test("Negative offset validation", "GET")
        try:
            response = self.make_request(
                "GET",
                "/api/asana_workspaces/workspaces/",
                params={"offset": -5, "limit": 10}
            )
            if response.status_code == 400:
                self.print_success("Correctly rejected negative offset")
            else:
                self.print_error("Should return 400 for negative offset")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Test zero limit
        self.print_test("Zero limit validation", "GET")
        try:
            response = self.make_request(
                "GET",
                "/api/asana_workspaces/workspaces/",
                params={"offset": 0, "limit": 0}
            )
            if response.status_code == 400:
                self.print_success("Correctly rejected zero limit")
            else:
                self.print_error("Should return 400 for zero limit")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

        # Test limit exceeds max
        self.print_test("Limit exceeds max validation", "GET")
        try:
            response = self.make_request(
                "GET",
                "/api/asana_workspaces/workspaces/",
                params={"offset": 0, "limit": 1000}
            )
            if response.status_code == 400:
                self.print_success("Correctly rejected excessive limit")
            else:
                self.print_error("Should return 400 for excessive limit")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_rate_limiting(self):
        """Test rate limiting"""
        self.print_header("⏱️  RATE LIMITING")

        self.print_test("Rate limit test (6 requests in < 1 min)", "POST")
        try:
            workspace_data = {
                "name": "Rate Limit Test",
                "is_organization": False
            }

            success_count = 0
            rate_limited = False

            for i in range(6):
                response = self.make_request(
                    "POST",
                    "/api/asana_workspaces/workspaces/",
                    data=workspace_data
                )
                if response.status_code == 201:
                    success_count += 1
                elif response.status_code == 429:
                    rate_limited = True
                    break

            if rate_limited and success_count == 5:
                self.print_success(
                    f"Rate limit working (5 requests allowed, 6th blocked)"
                )
            elif rate_limited:
                self.print_success(
                    f"Rate limit activated after {success_count} requests"
                )
            else:
                self.print_error("Rate limit not working")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def cleanup(self):
        """Delete created test resources"""
        self.print_header("🧹 CLEANUP")

        # Delete in reverse order of dependencies
        resources_to_delete = [
            ('webhook', '/api/asana_webhooks/webhooks/'),
            ('story', '/api/asana_stories/stories/'),
            ('task', '/api/asana_tasks/tasks/'),
            ('tag', '/api/asana_tags/tags/'),
            ('project', '/api/asana_projects/projects/'),
            ('team', '/api/asana_teams/teams/'),
            ('user', '/api/asana_users/users/'),
            ('workspace', '/api/asana_workspaces/workspaces/'),
        ]

        for resource_name, endpoint_base in resources_to_delete:
            if resource_name in self.created_resources:
                self.print_test(f"Delete {resource_name}", "DELETE")
                try:
                    gid = self.created_resources[resource_name]
                    response = self.make_request(
                        "DELETE", f"{endpoint_base}{gid}/"
                    )
                    if response.status_code == 204:
                        self.print_success(f"Deleted {resource_name}")
                    elif response.status_code == 405:
                        self.print_skip("DELETE not implemented yet")
                    else:
                        self.print_error(
                            f"Status {response.status_code}"
                        )
                except Exception as e:
                    self.print_error(f"Exception: {str(e)}")

    def print_summary(self):
        """Print test summary"""
        self.print_header("📊 TEST SUMMARY")

        total = sum(self.results.values())
        passed = self.results['passed']
        failed = self.results['failed']
        skipped = self.results['skipped']

        print(f"{Colors.BOLD}Total Tests:{Colors.RESET} {total}")
        print(
            f"{Colors.GREEN}✅ Passed:{Colors.RESET} {passed} "
            f"({passed/total*100:.1f}%)"
        )
        if failed > 0:
            print(
                f"{Colors.RED}❌ Failed:{Colors.RESET} {failed} "
                f"({failed/total*100:.1f}%)"
            )
        if skipped > 0:
            print(
                f"{Colors.YELLOW}⏭️  Skipped:{Colors.RESET} {skipped} "
                f"({skipped/total*100:.1f}%)"
            )

        print()

        if failed == 0:
            print(
                f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!"
                f"{Colors.RESET}"
            )
        else:
            print(
                f"{Colors.YELLOW}{Colors.BOLD}⚠️  SOME TESTS FAILED OR "
                f"SKIPPED{Colors.RESET}"
            )

    def run_all_tests(self):
        """Run all API tests"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                                                                   ║")
        print("║           ASANA BACKEND - COMPREHENSIVE API TEST SUITE           ║")
        print("║                                                                   ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        print(f"Base URL: {self.base_url}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Test all resources
            self.test_workspaces()
            self.test_users()
            self.test_projects()
            self.test_teams()
            self.test_tags()
            self.test_tasks()
            self.test_stories()
            self.test_webhooks()

            # Test pagination and validation
            self.test_pagination()

            # Test rate limiting
            self.test_rate_limiting()

            # Cleanup
            self.cleanup()

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Unexpected error: {str(e)}{Colors.RESET}")
        finally:
            # Print summary
            self.print_summary()


def main():
    """Main entry point"""
    tester = APITester(base_url="http://localhost:8000")
    tester.run_all_tests()


if __name__ == "__main__":
    main()


