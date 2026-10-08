"""
Response Helper
Provides standardized response formatting for API endpoints using FastAPI's JSONResponse.
"""

from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    """
    Build a standardized success JSONResponse.

    Args:
        data: The response payload.
        message: A human-readable success message.
        status_code: HTTP status code for the response.

    Returns:
        JSONResponse with success=True, message, data, and status_code.
    """
    content = {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code,
    }
    return JSONResponse(status_code=status_code, content=content)


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    errors: Optional[list] = None,
) -> JSONResponse:
    """
    Build a standardized error JSONResponse.

    Args:
        message: A human-readable error message.
        status_code: HTTP status code for the response.
        errors: Optional list of detailed error descriptions.

    Returns:
        JSONResponse with success=False, message, and optional errors.
    """
    content = {
        "success": False,
        "message": message,
        "status_code": status_code,
    }
    if errors:
        content["errors"] = errors
    return JSONResponse(status_code=status_code, content=content)


def paginated_response(
    data: list,
    total: int,
    page: int,
    per_page: int,
    message: str = "Success",
) -> JSONResponse:
    """
    Build a standardized paginated JSONResponse.

    Args:
        data: List of items for the current page.
        total: Total number of items across all pages.
        page: Current page number (1-based).
        per_page: Number of items per page.
        message: A human-readable success message.

    Returns:
        JSONResponse with pagination metadata and data.
    """
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    content = {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }
    return JSONResponse(status_code=200, content=content)
