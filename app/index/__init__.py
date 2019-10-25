from flask import Blueprint, render_template
from app.func import login_required

bp = Blueprint('index', __name__, template_folder='templates')

@bp.route('/index')
@bp.route('/')
@login_required
def index():
    return render_template('index.html', title='Группы и студенты')

