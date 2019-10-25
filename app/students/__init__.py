from flask import Blueprint
from . import views

bp = Blueprint('students', __name__, template_folder='templates')
options = {'url_prefix': '/student'}

bp.add_url_rule('/student', view_func=views.studentform, 
                methods=['GET', 'POST'])
bp.add_url_rule('/list', view_func=views.get_students, methods=['GET', 'POST'])
bp.add_url_rule('/del', view_func=views.delstudent, 
                methods=['GET', 'POST'])

