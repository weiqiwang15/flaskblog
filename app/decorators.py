from functools import wraps
from flask import abort
from flask_login import current_user
from app.models.role import Permission


def permission_required(permission):
    # 定义装饰器
    def decorator(f):
        @wraps(f)
        # 定义装饰后的函数
        def decorated_function(*args, **kwargs):
            # 如果当前用户没有给定的 permission
            if not current_user.can(permission):
                # 转到 403 错误页面
                abort(403)
            # 如果当前用户有给定的 permission
            else:
                # 返回被装饰的函数
                return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)