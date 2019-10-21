from flask import render_template
from app.analis.func import analis_gr

def countstud():
    req = analis_gr()
    return render_template('kolvostud.html', req=req, 
                           title = 'Количество студентов')

