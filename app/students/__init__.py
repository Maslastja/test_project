from flask import Blueprint
from . import views

bp = Blueprint('students', __name__, template_folder='templates')
options = {'url_prefix': '/student'}

bp.add_url_rule('/add', view_func=views.addstudent, 
                methods=['GET', 'POST'])
bp.add_url_rule('/list', view_func=views.get_students)
bp.add_url_rule('/up', view_func=views.upstudent, 
                methods=['GET', 'POST'])
bp.add_url_rule('/del', view_func=views.delstudent, 
                methods=['GET', 'POST'])

