from flask import Blueprint
from . import views

bp = Blueprint('analis', __name__, template_folder='templates')
bp.add_url_rule('/countstud', view_func=views.countstud)
 
