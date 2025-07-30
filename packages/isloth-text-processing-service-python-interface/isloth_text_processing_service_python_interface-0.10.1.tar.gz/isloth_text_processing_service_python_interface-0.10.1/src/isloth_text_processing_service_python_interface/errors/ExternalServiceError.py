"""
ExternalServiceError.py
-----------------------
Defines a 502 error raised when a downstream external service fails.
"""

from typing import Any, Optional
from isloth_python_common_lib.enums.ErrorCode import ErrorCode
from isloth_python_common_lib.enums.StatusCode import StatusCode
from isloth_python_common_lib.errors.AppError import AppError


class ExternalServiceError(AppError):
    """
    Raised when an external dependency or third-party service fails.

    Attributes
    ----------
    service : str
        The name of the external service that failed.
    message : str
        Descriptive message for the failure.
    status_code : StatusCode
        Always 502 (BAD_GATEWAY).
    details : Any, optional
        Extra error context (logs, stack trace, etc.).
    """

    def __init__(self, service: str, message: str = 'External service error', details: Optional[Any] = None):
        super().__init__(message, StatusCode.BAD_GATEWAY, details)
        self.add_error({
            'code': ErrorCode.EXTERNAL_SERVICE_ERROR.value,
            'field': service,
            'message': message
        })
