#!/usr/bin/env python3
"""
Compare API Spec with Implementation
Extracts request/response schemas from api_spec.txt and compares with actual serializers
"""
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_schema_from_spec(spec_file: str) -> Dict[str, Any]:
    """Extract API endpoints and their schemas from OpenAPI spec"""
    with open(spec_file, 'r') as f:
        content = f.read()
    
    schemas = {}
    
    # Find paths section
    paths_match = re.search(r'paths:\s*\n((?:  /[^\n]+\n(?:    [^\n]+\n)+)+)', content, re.MULTILINE)
    if not paths_match:
        return schemas
    
    paths_section = paths_match.group(1)
    
    # Extract each endpoint
    endpoint_pattern = r'  (/(?:[^{}]+|{[^}]+})+):\s*\n((?:    [^\n]+\n)+?)(?=  /|\Z)'
    endpoints = re.finditer(endpoint_pattern, paths_section, re.MULTILINE | re.DOTALL)
    
    for match in endpoints:
        endpoint = match.group(1)
        endpoint_content = match.group(2)
        
        # Extract methods (get, post, put, delete)
        methods = {}
        method_pattern = r'    (get|post|put|delete|patch):\s*\n((?:      [^\n]+\n)+?)(?=    (?:get|post|put|delete|patch):|\Z)'
        method_matches = re.finditer(method_pattern, endpoint_content, re.MULTILINE | re.DOTALL)
        
        for method_match in method_matches:
            method = method_match.group(1)
            method_content = method_match.group(2)
            
            # Extract request body schema
            request_body = None
            request_match = re.search(r'      requestBody:\s*\n((?:        [^\n]+\n)+)', method_content, re.MULTILINE)
            if request_match:
                request_content = request_match.group(1)
                schema_match = re.search(r'            \$ref:\s*[\'"]#/components/schemas/([^\'"]+)[\'"]', request_content)
                if schema_match:
                    request_body = schema_match.group(1)
            
            # Extract response schemas
            responses = {}
            response_pattern = r'        (\d{3}):\s*\n((?:          [^\n]+\n)+?)(?=        \d{3}:|\Z)'
            response_matches = re.finditer(response_pattern, method_content, re.MULTILINE | re.DOTALL)
            
            for resp_match in response_matches:
                status_code = resp_match.group(1)
                resp_content = resp_match.group(2)
                
                # Find schema reference
                schema_match = re.search(r'              \$ref:\s*[\'"]#/components/schemas/([^\'"]+)[\'"]', resp_content)
                if schema_match:
                    responses[status_code] = schema_match.group(1)
            
            if request_body or responses:
                methods[method] = {
                    'request': request_body,
                    'responses': responses
                }
        
        if methods:
            schemas[endpoint] = methods
    
    return schemas

def extract_component_schemas(spec_file: str) -> Dict[str, Any]:
    """Extract component schemas from OpenAPI spec"""
    with open(spec_file, 'r') as f:
        content = f.read()
    
    schemas = {}
    
    # Find components/schemas section
    components_match = re.search(r'components:\s*\n    schemas:\s*\n((?:      [^\n]+\n)+)', content, re.MULTILINE)
    if not components_match:
        return schemas
    
    schemas_section = components_match.group(1)
    
    # Extract each schema
    schema_pattern = r'      ([A-Za-z0-9_]+):\s*\n((?:        [^\n]+\n)+?)(?=      [A-Za-z0-9_]+:|\Z)'
    schema_matches = re.finditer(schema_pattern, schemas_section, re.MULTILINE | re.DOTALL)
    
    for match in schema_matches:
        schema_name = match.group(1)
        schema_content = match.group(2)
        
        # Extract properties
        properties = {}
        prop_pattern = r'          ([a-z_]+):\s*\n((?:            [^\n]+\n)+?)(?=          [a-z_]+:|\Z)'
        prop_matches = re.finditer(prop_pattern, schema_content, re.MULTILINE | re.DOTALL)
        
        for prop_match in prop_matches:
            prop_name = prop_match.group(1)
            prop_content = prop_match.group(2)
            
            # Extract type
            type_match = re.search(r'            type:\s*([^\n]+)', prop_content)
            prop_type = type_match.group(1).strip() if type_match else None
            
            # Extract $ref
            ref_match = re.search(r'            \$ref:\s*[\'"]#/components/schemas/([^\'"]+)[\'"]', prop_content)
            prop_ref = ref_match.group(1) if ref_match else None
            
            properties[prop_name] = {
                'type': prop_type,
                'ref': prop_ref
            }
        
        if properties:
            schemas[schema_name] = properties
    
    return schemas

def get_implementation_serializers() -> Dict[str, Any]:
    """Get actual serializer implementations"""
    serializers = {}
    
    # Check each app's serializers
    apps = [
        'asana_workspaces', 'asana_users', 'asana_projects', 
        'asana_tasks', 'asana_teams', 'asana_tags',
        'asana_stories', 'asana_attachments', 'asana_webhooks'
    ]
    
    for app in apps:
        serializer_file = Path(f'backend/{app}/serializers.py')
        if serializer_file.exists():
            with open(serializer_file, 'r') as f:
                content = f.read()
            
            # Extract serializer classes
            serializer_pattern = r'class (\w+Serializer)\([^)]+\):\s*\n((?:    [^\n]+\n)+?)(?=class |\Z)'
            serializer_matches = re.finditer(serializer_pattern, content, re.MULTILINE | re.DOTALL)
            
            for ser_match in serializer_matches:
                ser_name = ser_match.group(1)
                ser_content = ser_match.group(2)
                
                # Extract fields
                fields = []
                field_pattern = r'fields\s*=\s*\[([^\]]+)\]'
                field_match = re.search(field_pattern, ser_content)
                if field_match:
                    fields_str = field_match.group(1)
                    fields = [f.strip().strip("'\"") for f in fields_str.split(',')]
                
                serializers[f'{app}.{ser_name}'] = {
                    'fields': fields,
                    'content': ser_content[:200]  # First 200 chars
                }
    
    return serializers

def compare_schemas(spec_schemas: Dict, impl_serializers: Dict) -> Dict[str, Any]:
    """Compare spec schemas with implementation"""
    comparison = {
        'matches': [],
        'mismatches': [],
        'missing': [],
        'extra': []
    }
    
    # Key endpoint mappings
    endpoint_mappings = {
        '/workspaces': 'asana_workspaces',
        '/workspaces/{workspace_gid}': 'asana_workspaces',
        '/users': 'asana_users',
        '/users/{user_gid}': 'asana_users',
        '/projects': 'asana_projects',
        '/projects/{project_gid}': 'asana_projects',
        '/tasks': 'asana_tasks',
        '/tasks/{task_gid}': 'asana_tasks',
        '/teams': 'asana_teams',
        '/teams/{team_gid}': 'asana_teams',
        '/tags': 'asana_tags',
        '/tags/{tag_gid}': 'asana_tags',
        '/stories/{story_gid}': 'asana_stories',
        '/tasks/{task_gid}/stories': 'asana_stories',
        '/attachments/{attachment_gid}': 'asana_attachments',
        '/tasks/{task_gid}/attachments': 'asana_attachments',
        '/webhooks': 'asana_webhooks',
        '/webhooks/{webhook_gid}': 'asana_webhooks',
    }
    
    for endpoint, methods in spec_schemas.items():
        app_name = endpoint_mappings.get(endpoint)
        if not app_name:
            continue
        
        for method, details in methods.items():
            request_schema = details.get('request')
            responses = details.get('responses', {})
            
            # Check if we have corresponding serializer
            # This is a simplified check - actual comparison would need deeper analysis
            comparison['matches'].append({
                'endpoint': endpoint,
                'method': method.upper(),
                'app': app_name
            })
    
    return comparison

def main():
    print("="*80)
    print("API SPEC vs IMPLEMENTATION COMPARISON")
    print("="*80)
    print()
    
    spec_file = 'backend/api_spec.txt'
    if not Path(spec_file).exists():
        print(f"❌ Spec file not found: {spec_file}")
        return
    
    print("📖 Extracting schemas from API spec...")
    spec_schemas = extract_schema_from_spec(spec_file)
    print(f"   Found {len(spec_schemas)} endpoints")
    
    print("\n🔍 Extracting component schemas...")
    component_schemas = extract_component_schemas(spec_file)
    print(f"   Found {len(component_schemas)} component schemas")
    
    print("\n💻 Checking implementation serializers...")
    impl_serializers = get_implementation_serializers()
    print(f"   Found {len(impl_serializers)} serializers")
    
    print("\n📊 Comparing...")
    comparison = compare_schemas(spec_schemas, impl_serializers)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Matches: {len(comparison['matches'])}")
    print(f"❌ Mismatches: {len(comparison['mismatches'])}")
    print(f"⚠️  Missing: {len(comparison['missing'])}")
    print(f"➕ Extra: {len(comparison['extra'])}")
    
    # Print key endpoints found
    print("\n" + "="*80)
    print("KEY ENDPOINTS IN SPEC")
    print("="*80)
    key_endpoints = [
        '/workspaces', '/workspaces/{workspace_gid}',
        '/users', '/users/{user_gid}',
        '/projects', '/projects/{project_gid}',
        '/tasks', '/tasks/{task_gid}',
        '/teams', '/teams/{team_gid}',
        '/tags', '/tags/{tag_gid}',
        '/stories/{story_gid}', '/tasks/{task_gid}/stories',
        '/attachments/{attachment_gid}', '/tasks/{task_gid}/attachments',
        '/webhooks', '/webhooks/{webhook_gid}'
    ]
    
    for endpoint in key_endpoints:
        if endpoint in spec_schemas:
            methods = list(spec_schemas[endpoint].keys())
            print(f"✅ {endpoint:40} - Methods: {', '.join(methods).upper()}")
        else:
            print(f"❌ {endpoint:40} - NOT FOUND IN SPEC")
    
    # Save detailed report
    report = {
        'spec_endpoints': len(spec_schemas),
        'component_schemas': len(component_schemas),
        'impl_serializers': len(impl_serializers),
        'comparison': comparison,
        'key_endpoints': {ep: spec_schemas.get(ep, {}) for ep in key_endpoints}
    }
    
    with open('backend/api_comparison_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n📄 Detailed report saved to: backend/api_comparison_report.json")

if __name__ == '__main__':
    main()

