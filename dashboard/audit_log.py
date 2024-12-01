import logging
import functools

# Set up logger
logger = logging.getLogger(__name__)

# Create a decorator to log user actions
def audit_log(action_type, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs_):
            result = func(*args, **kwargs_)
            # Log the action with function name and any extra info
            logger.info(f"{action_type} performed. Function: {func.__name__}, Args: {args}, Kwargs: {kwargs_}")
            return result
        return wrapper
    return decorator