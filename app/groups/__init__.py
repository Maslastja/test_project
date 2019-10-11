from flask import Blueprint
from . import views

bp = Blueprint('groups', __name__, template_folder='templates')
options = {'url_prefix': '/group'}

bp.add_url_rule('/add', view_func=views.add_group_form, 
                methods=['GET', 'POST'])
bp.add_url_rule('/list', view_func=views.get_groups)
bp.add_url_rule('/up', view_func=views.upgroup, methods=['GET', 'POST'])
bp.add_url_rule('/del', view_func=views.delgroup, methods=['GET', 'POST'])

bp.add_url_rule('/test', view_func=views.test_secr)

