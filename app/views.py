from flask import render_template
from app.func import login_required

#@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Группы и студенты')

