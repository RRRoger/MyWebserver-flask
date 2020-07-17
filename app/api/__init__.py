from flask import Blueprint
api = Blueprint('api', __name__)

from . import authentication
from . import posts
from . import users
from . import comments
from . import errors

