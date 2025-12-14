from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Structured error detail following RFC 7807 Problem Details"""

    type: str  # URI reference that identifies the problem type
    title: str  # Short, human-readable summary
    status: int  # HTTP status code
    detail: str  # Human-readable explanation specific to this occurrence
    instance: str  # URI reference that identifies the specific occurrence
    timestamp: str  # ISO 8601 timestamp
    request_id: Optional[str] = None  # For tracking/debugging
    errors: Optional[dict[str, list[str]]] = None  # Field-specific validation errors


def create_error_response(
    status: int,
    title: str,
    detail: str,
    error_type: str = "about:blank",
    instance: str = "",
    request_id: Optional[str] = None,
    validation_errors: Optional[dict[str, list[str]]] = None,
) -> dict:
    """
    Create a standardized error response.

    Args:
        status: HTTP status code
        title: Short error summary
        detail: Detailed error message
        error_type: URI identifying the error type (default: about:blank)
        instance: URI identifying this specific error occurrence
        request_id: Optional request ID for tracking
        validation_errors: Optional field-level validation errors

    Returns:
        Dictionary containing structured error information
    """
    error = {
        "type": error_type,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if request_id:
        error["request_id"] = request_id

    if validation_errors:
        error["errors"] = validation_errors

    return error


# Common error templates
class ErrorTemplates:
    """Pre-defined error templates for common scenarios"""

    @staticmethod
    def not_found(resource: str, resource_id: str, instance: str = "") -> dict:
        return create_error_response(
            status=404,
            title="Resource Not Found",
            detail=f"{resource} with ID '{resource_id}' was not found.",
            error_type="https://api.example.com/errors/not-found",
            instance=instance,
        )

    @staticmethod
    def validation_error(errors: dict[str, list[str]], instance: str = "") -> dict:
        return create_error_response(
            status=422,
            title="Validation Error",
            detail="One or more fields failed validation.",
            error_type="https://api.example.com/errors/validation",
            instance=instance,
            validation_errors=errors,
        )

    @staticmethod
    def unauthorized(
        detail: str = "Authentication required.", instance: str = ""
    ) -> dict:
        return create_error_response(
            status=401,
            title="Unauthorized",
            detail=detail,
            error_type="https://api.example.com/errors/unauthorized",
            instance=instance,
        )

    @staticmethod
    def forbidden(
        detail: str = "You don't have permission to access this resource.",
        instance: str = "",
    ) -> dict:
        return create_error_response(
            status=403,
            title="Forbidden",
            detail=detail,
            error_type="https://api.example.com/errors/forbidden",
            instance=instance,
        )

    @staticmethod
    def internal_error(
        detail: str = "An unexpected error occurred.",
        instance: str = "",
        request_id: Optional[str] = None,
    ) -> dict:
        return create_error_response(
            status=500,
            title="Internal Server Error",
            detail=detail,
            error_type="https://api.example.com/errors/internal",
            instance=instance,
            request_id=request_id,
        )

    @staticmethod
    def bad_request(detail: str, instance: str = "") -> dict:
        return create_error_response(
            status=400,
            title="Bad Request",
            detail=detail,
            error_type="https://api.example.com/errors/bad-request",
            instance=instance,
        )

    @staticmethod
    def conflict(resource: str, detail: str, instance: str = "") -> dict:
        return create_error_response(
            status=409,
            title="Conflict",
            detail=f"{resource} conflict: {detail}",
            error_type="https://api.example.com/errors/conflict",
            instance=instance,
        )

    @staticmethod
    def rate_limit_exceeded(retry_after: int, instance: str = "") -> dict:
        error = create_error_response(
            status=429,
            title="Rate Limit Exceeded",
            detail=f"Too many requests. Please retry after {retry_after} seconds.",
            error_type="https://api.example.com/errors/rate-limit",
            instance=instance,
        )
        error["retry_after"] = retry_after
        return error
