"""
API Blueprint starting point
"""

from flask import Blueprint

api_page = Blueprint('api', __name__, url_prefix='/api')
