"""
Admin blueprint
"""

from flask import Blueprint
from admin import views

admin_page = Blueprint('admin', __name__, url_prefix='/admin',
                       template_folder='templates')
define = views.define
