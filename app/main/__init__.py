from flask import Blueprint
main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission
from . import common
from . import test_layui
from . import hs_user_api
from . import hs_user_forms
from . import hs_role_forms
from . import hs_role_api
from . import hs_model_api
from . import hs_model_forms
from . import hs_api_log_api
from . import hs_api_log_forms

from . import hs_bilibili_bv_api
from . import hs_bilibili_bv_forms


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
