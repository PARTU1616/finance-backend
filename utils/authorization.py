from functools import wraps
from flask import session, jsonify

def requires_auth(roles=None):
    """
    Decorator to enforce authentication and role-based authorization.
    
    Args:
        roles (list): List of allowed roles (e.g., ['Admin', 'Analyst'])
                     If None, only authentication is required
    
    Returns:
        401 if not authenticated
        403 if authenticated but lacks required role
        Proceeds to route handler if authorized
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = session.get('user_id')
            user_role = session.get('role')
            
            if not user_id:
                return jsonify(ok=False, error="Unauthorized", msg="Please log in"), 401
            
            if roles and user_role not in roles:
                return jsonify(ok=False, error="Forbidden", msg=f"This action requires one of: {', '.join(roles)}"), 403
            
            return f(*args, **kwargs)
        return decorated
    return wrapper
