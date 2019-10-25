from flask import Blueprint
from . import views

bp = Blueprint('groups', __name__, template_folder='templates')
options = {'url_prefix': '/group'}

bp.add_url_rule('/group', view_func=views.groupform, methods=['GET', 'POST'])
bp.add_url_rule('/list', view_func=views.get_groups, methods=['GET', 'POST'])

bp.add_url_rule('/test', view_func=views.test_secr)
