from flask import Blueprint
from . import views

bp = Blueprint('analis', __name__, template_folder='templates')
options = {'url_prefix': '/analis'}

bp.add_url_rule('/countstud', view_func=views.countstud)
 
