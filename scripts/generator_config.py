"""
Configuration for Django code generator.
"""

from typing import Dict, Any

# Resource name mappings from OpenAPI tags to Django app names
RESOURCE_APP_MAPPING = {
    'tasks': 'asana_tasks',
    'projects': 'asana_projects',
    'workspaces': 'asana_workspaces',
    'users': 'asana_users',
    'teams': 'asana_teams',
    'tags': 'asana_tags',
    'stories': 'asana_stories',
    'attachments': 'asana_attachments',
    'webhooks': 'asana_webhooks',
    'portfolios': 'asana_portfolios',
    'goals': 'asana_goals',
    'custom fields': 'asana_custom_fields',
    'sections': 'asana_sections',
    'status updates': 'asana_status_updates',
    'memberships': 'asana_memberships',
    'project briefs': 'asana_project_briefs',
    'project statuses': 'asana_project_statuses',
    'user task lists': 'asana_user_task_lists',
    'time tracking': 'asana_time_tracking',
}

# OpenAPI type to Django field type mapping
OPENAPI_TO_DJANGO_FIELD = {
    'string': 'CharField',
    'integer': 'IntegerField',
    'number': 'FloatField',
    'boolean': 'BooleanField',
    'array': 'JSONField',
    'object': 'JSONField',
}

# OpenAPI type to DRF serializer field mapping
OPENAPI_TO_DRF_FIELD = {
    'string': 'CharField',
    'integer': 'IntegerField',
    'number': 'FloatField',
    'boolean': 'BooleanField',
    'array': 'ListField',
    'object': 'DictField',
}

# OpenAPI format to Python type mapping
OPENAPI_FORMAT_TO_PYTHON_TYPE = {
    'date': 'str',
    'date-time': 'str',
    'email': 'str',
    'uri': 'str',
    'uuid': 'str',
    'int32': 'int',
    'int64': 'int',
    'float': 'float',
    'double': 'float',
}

# HTTP method to function name mapping
HTTP_METHOD_TO_FUNCTION = {
    'GET': 'get',
    'POST': 'post',
    'PUT': 'put',
    'DELETE': 'delete',
    'PATCH': 'patch',
}

# Rate limit by HTTP method
DEFAULT_RATE_LIMITS = {
    'GET': '10/s',
    'POST': '5/s',
    'PUT': '5/s',
    'DELETE': '3/s',
    'PATCH': '5/s',
}

# Success status codes by HTTP method
SUCCESS_STATUS_CODES = {
    'GET': '200_OK',
    'POST': '201_CREATED',
    'PUT': '200_OK',
    'DELETE': '204_NO_CONTENT',
    'PATCH': '200_OK',
}

# Common error response imports
ERROR_RESPONSE_FUNCTIONS = [
    'not_found_error',
    'invalid_gid_error',
    'missing_field_error',
    'server_error',
]


def get_app_name(resource: str) -> str:
    """
    Get Django app name for resource.
    
    Args:
        resource: Resource name from OpenAPI
        
    Returns:
        Django app name
    """
    resource_lower = resource.lower()
    
    # Check exact match
    if resource_lower in RESOURCE_APP_MAPPING:
        return RESOURCE_APP_MAPPING[resource_lower]
    
    # Check partial match
    for key, value in RESOURCE_APP_MAPPING.items():
        if key in resource_lower:
            return value
    
    # Default: add asana_ prefix
    resource_clean = resource_lower.replace(' ', '_')
    return f'asana_{resource_clean}'


def get_model_name(resource: str) -> str:
    """
    Get Django model name for resource.
    
    Args:
        resource: Resource name
        
    Returns:
        Model class name (PascalCase, singular)
    """
    # Remove plural 's'
    singular = resource.rstrip('s')
    
    # Convert to PascalCase
    parts = singular.split('_')
    return ''.join(word.capitalize() for word in parts)


def get_operation_type(operation_id: str, method: str, path: str) -> str:
    """
    Determine operation type from operation ID, method, and path.
    
    Args:
        operation_id: OpenAPI operation ID
        method: HTTP method
        path: API path
        
    Returns:
        Operation type (create, get, update, delete, list, action)
    """
    operation_lower = operation_id.lower()
    
    # Direct mappings
    if any(x in operation_lower for x in ['create', 'add']):
        return 'create'
    if any(x in operation_lower for x in ['get', 'find', 'search']):
        if method == 'GET' and '{' not in path:
            return 'list'
        return 'get'
    if any(x in operation_lower for x in ['update', 'modify', 'edit']):
        return 'update'
    if any(x in operation_lower for x in ['delete', 'remove']):
        return 'delete'
    if 'list' in operation_lower:
        return 'list'
    
    # Method-based fallback
    if method == 'GET':
        return 'list' if '{' not in path else 'get'
    elif method == 'POST':
        return 'create'
    elif method in ['PUT', 'PATCH']:
        return 'update'
    elif method == 'DELETE':
        return 'delete'
    
    return 'action'


def generate_class_name(operation_id: str, suffix: str = 'View') -> str:
    """
    Generate Python class name from operation ID.
    
    Args:
        operation_id: OpenAPI operation ID
        suffix: Class name suffix
        
    Returns:
        PascalCase class name
    """
    # Convert to words
    words = []
    current_word = []
    
    for char in operation_id:
        if char.isupper() and current_word:
            words.append(''.join(current_word))
            current_word = [char]
        elif char in ['_', '-']:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
        else:
            current_word.append(char)
    
    if current_word:
        words.append(''.join(current_word))
    
    # Capitalize each word
    class_name = ''.join(word.capitalize() for word in words)
    
    # Add suffix if not present
    if not class_name.endswith(suffix):
        class_name += suffix
    
    return class_name


def generate_function_name(operation_id: str) -> str:
    """
    Generate Python function name from operation ID.
    
    Args:
        operation_id: OpenAPI operation ID
        
    Returns:
        snake_case function name
    """
    # Insert underscores before capitals
    result = []
    for i, char in enumerate(operation_id):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    
    function_name = ''.join(result)
    
    # Clean up
    function_name = function_name.replace('-', '_')
    function_name = function_name.replace('__', '_')
    
    return function_name


def get_python_type(openapi_type: str, format: str = None) -> str:
    """
    Convert OpenAPI type to Python type hint.
    
    Args:
        openapi_type: OpenAPI type
        format: OpenAPI format
        
    Returns:
        Python type hint string
    """
    if format and format in OPENAPI_FORMAT_TO_PYTHON_TYPE:
        return OPENAPI_FORMAT_TO_PYTHON_TYPE[format]
    
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'array': 'List',
        'object': 'Dict',
    }
    
    return type_mapping.get(openapi_type, 'Any')


def should_skip_endpoint(endpoint: Dict) -> bool:
    """
    Determine if endpoint should be skipped.
    
    Args:
        endpoint: Endpoint data from OpenAPI
        
    Returns:
        True if should skip
    """
    # Skip deprecated
    if endpoint.get('deprecated', False):
        return True
    
    # Skip batch API
    if '/batch' in endpoint.get('path', ''):
        return True
    
    # Skip audit log (requires service account)
    if 'audit' in endpoint.get('path', '').lower():
        return True
    
    return False

