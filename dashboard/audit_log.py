from .models import Audit_Log
from django.contrib.auth.models import User
import functools

def audit_log(action_type, object_type, user=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Handle the user assignment (assuming the first argument is the request or object with a user attribute)
            user = None
            if hasattr(args[0], 'user'):
                user = args[0].user
            
            # Ensure that user is a valid User object (if not, set to None)
            if not isinstance(user, User):
                user = None  # Fallback to None if user is not a valid User object
            
            # Call the original function
            result = func(*args, **kwargs)
            
            # Create the audit log entry
            Audit_Log.objects.create(
                action_type=action_type,
                user=user,
                object_type=object_type,
                details=kwargs  # Store detailed information in `details`
            )
            
            return result
        return wrapper
    return decorator
