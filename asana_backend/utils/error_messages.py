"""
Standard error message helpers for Asana API responses
"""

def invalid_gid_error(field_name: str = "gid") -> dict:
    """Return standard invalid GID error"""
    return {
        'errors': [{
            'message': f'{field_name}: Invalid GID format',
            'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
            'phrase': '6 sad squid snuggle softly'
        }]
    }

def not_found_error(resource_type: str, gid: str = None) -> dict:
    """Return standard not found error"""
    message = f"{resource_type.capitalize()} does not exist"
    if gid:
        message = f"{resource_type.capitalize()} with GID '{gid}' does not exist"
    
    return {
        'errors': [{
            'message': message,
            'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
            'phrase': '6 sad squid snuggle softly'
        }]
    }

def bad_request_error(message: str) -> dict:
    """Return standard bad request error"""
    return {
        'errors': [{
            'message': message,
            'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
            'phrase': '6 sad squid snuggle softly'
        }]
    }

def conflict_error(message: str) -> dict:
    """Return standard conflict error"""
    return {
        'errors': [{
            'message': message,
            'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
            'phrase': '6 sad squid snuggle softly'
        }]
    }

def server_error(message: str = "Internal server error") -> dict:
    """Return standard server error"""
    return {
        'errors': [{
            'message': message,
            'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
            'phrase': '6 sad squid snuggle softly'
        }]
    }

