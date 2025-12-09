"""
Asana API Error Response Utility

Generates error responses matching the exact Asana API spec schema:
{
    "errors": [
        {
            "message": "Error message",
            "help": "Help URL",
            "phrase": "Random phrase for 500 errors"
        }
    ]
}
"""
import random


# Asana-style error phrases (used for 500 errors)
ERROR_PHRASES = [
    "6 sad squid snuggle softly",
    "3 angry ants argue always", 
    "5 blue birds bounce briskly",
    "4 quick quails quiver quietly",
    "7 red rabbits run rapidly",
    "2 green geckos gallop gracefully",
    "8 purple penguins parade proudly",
    "9 orange octopi operate optimally",
]

HELP_URL = "For more information on API status codes and how to handle them, read the docs on errors: https://developers.asana.com/docs/errors"


def generate_error_phrase():
    """Generate a random error phrase for 500 errors"""
    return random.choice(ERROR_PHRASES)


def create_error_response(message: str, include_help: bool = True, include_phrase: bool = False):
    """
    Create an error response matching Asana API spec.
    
    Args:
        message: The error message
        include_help: Include help URL (default True for all errors)
        include_phrase: Include phrase (only for 500 errors)
    
    Returns:
        dict: Error response in Asana format
    """
    error = {
        "message": message
    }
    
    if include_help:
        error["help"] = HELP_URL
    
    if include_phrase:
        error["phrase"] = generate_error_phrase()
    
    return {
        "errors": [error]
    }


def bad_request_error(message: str):
    """400 Bad Request error"""
    return create_error_response(message, include_help=True, include_phrase=False)


def unauthorized_error(message: str = "Not Authorized"):
    """401 Unauthorized error"""
    return create_error_response(message, include_help=True, include_phrase=False)


def forbidden_error(message: str = "Forbidden"):
    """403 Forbidden error"""
    return create_error_response(message, include_help=True, include_phrase=False)


def not_found_error(resource_type: str, gid: str):
    """404 Not Found error"""
    message = f"{resource_type}: Unknown object: {gid}"
    return create_error_response(message, include_help=True, include_phrase=False)


def rate_limit_error():
    """429 Too Many Requests error"""
    return create_error_response(
        "Rate limit exceeded. Please retry after some time.",
        include_help=True,
        include_phrase=False
    )


def server_error(message: str = "Server Error"):
    """500 Internal Server Error"""
    return create_error_response(message, include_help=True, include_phrase=True)


def missing_field_error(field_name: str):
    """Error for missing required field"""
    return bad_request_error(f"{field_name}: Missing input")


def invalid_field_error(field_name: str, reason: str):
    """Error for invalid field value"""
    return bad_request_error(f"{field_name}: {reason}")


def invalid_gid_error(resource_type: str):
    """Error for invalid GID format"""
    return bad_request_error(f"{resource_type}: Invalid GID format")
