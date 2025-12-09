"""
Rate limiting decorator for API views.
"""
import json
import re
from functools import wraps
from django.http import HttpResponse
from django_ratelimit import ALL, UNSAFE
from django_ratelimit.core import is_ratelimited

__all__ = ['ratelimit']

RATE_LIMIT_EXCEEDED = (
    "You've reached the maximum number of requests. Please try again after {wait_time}.",
    "RATE_LIMIT_EXCEEDED",
)


def ratelimit(group=None, key=None, rate=None, method=ALL, block=True):
    """
    Rate limit decorator for Django views.
    
    Args:
        group: Rate limit group name
        key: Key function to identify the client (e.g., 'ip', 'user')
        rate: Rate limit string (e.g., '5/m', '100/m', '1000/h')
        method: HTTP methods to rate limit (ALL, UNSAFE, or specific methods)
        block: Whether to block requests when rate limit is exceeded
    
    Usage:
        @ratelimit(key='ip', rate='5/m')
        def my_view(request):
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def _wrapped(*args, **kw):
            # Handle both function-based views and class-based views
            # For class methods: args = (self, request, ...)
            # For functions: args = (request, ...)
            if len(args) >= 2 and hasattr(args[0], '__class__'):
                # Likely a class method (first arg is self)
                request = args[1]
            elif len(args) >= 1:
                # Likely a function (first arg is request)
                request = args[0]
            else:
                raise ValueError("No request found in arguments")
            
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(
                request=request,
                group=group,
                fn=fn,
                key=key,
                rate=rate,
                method=method,
                increment=True
            )
            request.limited = ratelimited or old_limited
            
            if ratelimited and block:
                wait_time = convert_time_to_readable(rate.split("/")[1])
                body = {
                    "res_status": RATE_LIMIT_EXCEEDED[1],
                    "http_status_code": 429,
                    "response": RATE_LIMIT_EXCEEDED[0].format(
                        wait_time=wait_time
                    ),
                }
                data = json.dumps(body)
                return HttpResponse(data, status=429, content_type='application/json')
            
            return fn(*args, **kw)
        
        return _wrapped
    
    return decorator


def convert_time_to_readable(time_value: str) -> str:
    """
    Convert time values to human-readable format for rate limit messages.
    
    Args:
        time_value (str): Time value like '1m', '60s', '2hr', 'hr', 'm'
    
    Returns:
        str: Human-readable time format
    """
    if not time_value:
        return "a moment"
    
    time_value = str(time_value).strip().lower()
    
    match = re.match(r'^(\d*)(.*?)$', time_value)
    if not match:
        return "a moment"
    
    number_part = match.group(1)
    unit_part = match.group(2).strip()
    
    number = int(number_part) if number_part else 1
    
    unit_mappings = {
        's': 'second',
        'm': 'minute',
        'h': 'hour',
        'hr': 'hour',
        'hour': 'hour',
        'min': 'minute',
        'minute': 'minute',
        'sec': 'second',
        'second': 'second',
    }
    
    base_unit = unit_mappings.get(unit_part, 'moment')
    
    if base_unit == 'moment':
        return "a moment"
    
    if number == 1:
        return f"1 {base_unit}"
    
    plural_unit = base_unit if base_unit.endswith('s') else base_unit + 's'
    
    return f"{number} {plural_unit}"


# Export constants
ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE

