from functools import wraps
from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask import jsonify
from src.constants.http_status_codes import HTTP_403_FORBIDDEN


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if user.is_admin:
            return fn(*args, **kwargs)
        return jsonify(msg='Admins only!'), HTTP_403_FORBIDDEN
    return wrapper
