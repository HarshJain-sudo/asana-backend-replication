#!/usr/bin/env python3
"""
Comprehensive CRUD Implementation Script
Implements POST/PUT/DELETE for all remaining apps
"""

import os
import sys

# Configuration for each app
APPS_CONFIG = {
    'asana_projects': {
        'model': 'Project',
        'resource': 'project',
        'fields': {
            'required': ['name', 'workspace_gid'],
            'optional': ['team_gid', 'public', 'archived', 'color', 'notes', 'due_date', 'start_on']
        }
    },
    'asana_teams': {
        'model': 'Team',
        'resource': 'team',
        'fields': {
            'required': ['name', 'workspace_gid'],
            'optional': ['description']
        }
    },
    'asana_tags': {
        'model': 'Tag',
        'resource': 'tag',
        'fields': {
            'required': ['name', 'workspace_gid'],
            'optional': ['color']
        }
    },
    'asana_stories': {
        'model': 'Story',
        'resource': 'story',
        'fields': {
            'required': ['task_gid', 'text'],
            'optional': ['html_text', 'is_pinned']
        }
    },
    'asana_webhooks': {
        'model': 'Webhook',
        'resource': 'webhook',
        'fields': {
            'required': ['resource', 'resource_gid', 'target'],
            'optional': ['active']
        }
    }
}

def check_app_status(app_name):
    """Check what's implemented for an app"""
    print(f"\n{'='*60}")
    print(f"Checking {app_name}...")
    print(f"{'='*60}")
    
    # Check storage
    storage_file = f"{app_name}/storages/storage_implementation.py"
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            content = f.read()
        has_create = 'def create_' in content
        has_update = 'def update_' in content
        has_delete = 'def delete_' in content
        print(f"  Storage - Create: {'✅' if has_create else '❌'} "
              f"Update: {'✅' if has_update else '❌'} "
              f"Delete: {'✅' if has_delete else '❌'}")
    else:
        print(f"  Storage - ❌ Not found")
        
    # Check views
    views_path = f"{app_name}/views"
    if os.path.exists(views_path):
        subdirs = os.listdir(views_path)
        has_create_view = any('create' in d for d in subdirs)
        has_update_view = any('update' in d for d in subdirs)
        has_delete_view = any('delete' in d for d in subdirs)
        print(f"  Views - Create: {'✅' if has_create_view else '❌'} "
              f"Update: {'✅' if has_update_view else '❌'} "
              f"Delete: {'✅' if has_delete_view else '❌'}")
              
def main():
    print("="*60)
    print("COMPREHENSIVE CRUD IMPLEMENTATION STATUS CHECK")
    print("="*60)
    
    for app_name in APPS_CONFIG.keys():
        check_app_status(app_name)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print("\nApps that need implementation:")
    print("1. asana_projects - Views need POST/PUT/DELETE")
    print("2. asana_teams - Full CRUD needed")
    print("3. asana_tags - Full CRUD needed")
    print("4. asana_stories - Full CRUD needed (only POST/DELETE, no UPDATE)")
    print("5. asana_webhooks - Full CRUD needed (only POST/DELETE, no UPDATE)")
    print("\nNote: This script checks status. Implementation will be done separately.")

if __name__ == "__main__":
    main()


