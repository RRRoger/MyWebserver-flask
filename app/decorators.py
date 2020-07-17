from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

# def pm_required(f):
    
#     return permission_required(Permission.Publishing_SoftWare)(f) and \
#            permission_required(Permission.Permission.PreviewSoftware)(f)

# def fl_required(f):
#     return permission_required(Permission.Specify_Upgrade_Version)(f) and \
#             permission_required(Permission.Specify_Preupgrade_Version)(f) and \
#             permission_required(Permission.Add_Remove_Burn_Upgrade_Rsa_Pub_List)(f) and \
#             permission_required(Permission.Add_Remove_E2prom_Rsa_Pub_List)(f) 
                

