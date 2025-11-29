"""
Custom exception handlers for the API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            'error': {
                'message': get_error_message(response.data),
                'code': get_error_code(exc),
                'status': response.status_code,
            }
        }

        # Add detail if available
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['detail'] = response.data['detail']
            elif 'non_field_errors' in response.data:
                custom_response_data['error']['detail'] = response.data['non_field_errors']
            else:
                # Field-specific errors
                custom_response_data['error']['fields'] = response.data

        response.data = custom_response_data

    return response


def get_error_message(data):
    """Extract a simple error message from response data."""
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        elif 'non_field_errors' in data:
            return str(data['non_field_errors'][0]) if data['non_field_errors'] else 'An error occurred'
        else:
            # Get first error from any field
            for field, errors in data.items():
                if isinstance(errors, list) and errors:
                    return f"{field}: {errors[0]}"
                return str(errors)
    return str(data)


def get_error_code(exc):
    """Get error code from exception."""
    return exc.__class__.__name__


# Custom exceptions
class DevoException(Exception):
    """Base exception for DEVO-specific errors."""
    default_message = 'An error occurred'
    default_code = 'devo_error'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        super().__init__(self.message)


class AgentExecutionError(DevoException):
    """Raised when agent execution fails."""
    default_message = 'Agent execution failed'
    default_code = 'agent_execution_error'


class ContextAssemblyError(DevoException):
    """Raised when context assembly fails."""
    default_message = 'Failed to assemble context'
    default_code = 'context_assembly_error'


class LLMConnectionError(DevoException):
    """Raised when LLM connection fails."""
    default_message = 'Failed to connect to LLM'
    default_code = 'llm_connection_error'
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class SubscriptionLimitError(DevoException):
    """Raised when subscription limit is reached."""
    default_message = 'Subscription limit reached'
    default_code = 'subscription_limit_error'
    status_code = status.HTTP_402_PAYMENT_REQUIRED
