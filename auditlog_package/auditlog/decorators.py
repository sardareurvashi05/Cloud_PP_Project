from django.contrib.auth.models import User
from .models import Audit_Log
import functools
from typing import Callable, Any, Optional

def audit_log(action_type: str, object_type: str, user: Optional[User] = None) -> Callable:
    """
    A decorator that logs audit information when an action is performed on an object.

    Args:
        action_type (str): The type of the action (e.g., 'create', 'update', 'delete').
        object_type (str): The type of the object being acted upon (e.g., 'ModelName').
        user (Optional[User], optional): The user performing the action. Defaults to None.

    Returns:
        Callable: The decorated function that logs audit information.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Assign user from the first argument if it's an HttpRequest object (commonly passed as `request` in views)
            user = None
            if hasattr(args[0], 'user'):
                user = args[0].user  # Extract user from request or object

            # Ensure that the user is a valid User object, fallback to None if not
            if not isinstance(user, User):
                user = None
            
            # Execute the original function
            result = func(*args, **kwargs)
            
            # Create the audit log entry
            Audit_Log.objects.create(
                action_type=action_type,
                user=user,
                object_type=object_type,
                details=str(kwargs)  # Store detailed information in `details`
            )
            
            return result
        return wrapper
    return decorator