from flask import Blueprint
from . import views

bp = Blueprint('admin', __name__, template_folder='templates')
options = {'url_prefix': '/admin'}

bp.add_url_rule('/addusr', view_func=views.create_usr,
                methods=['GET', 'POST'])
 
