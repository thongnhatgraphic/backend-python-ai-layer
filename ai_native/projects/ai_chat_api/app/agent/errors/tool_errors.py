class ToolError(Exception):
    """Base exception for tool execution."""


class ToolValidationError(ToolError):
    """Tool arguments are invalid."""


class ToolExecutionError(ToolError):
    """Tool execution failed."""


class ToolExcutionLimitExceededError(ToolError):
    """Tool execution exceeded the maximum number of loops."""


class ToolTimeoutError(ToolExecutionError):
    """Tool execution timed out."""


class ToolTransientError(ToolExecutionError):
    """Tool failed due to a transient condition."""


class ToolPermanentError(ToolExecutionError):
    """Tool failed with a non-retryable error."""


class ToolPolicyError(ToolError):
    """Tool policy error."""
