from flask import render_template
from app.func import login_required
from app.analis.func import analis_gr

@login_required
def countstud():
    req = analis_gr()
    return render_template('kolvostud.html', req=req, 
                           title = 'Количество студентов')

