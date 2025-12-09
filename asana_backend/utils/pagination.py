"""
Pagination utilities.
"""
from typing import Dict, Any, List, Optional


def get_pagination_metadata(
    items: List[Any],
    offset: int,
    limit: int,
    total_count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate pagination metadata for response.
    """
    if total_count is None:
        total_count = len(items)

    return {
        'count': len(items),
        'offset': offset,
        'limit': limit,
        'total': total_count,
        'has_more': (offset + len(items)) < total_count
    }

