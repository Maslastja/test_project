from flask import render_template, request
from app.admin.func import create_user
from app.admin.forms import AddUserForm

def create_usr():
    form = AddUserForm(request.form or None)
    if request.method == 'POST' and form.validate():
        req = create_user()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('addusr.html', form=form,  
                               title='Добавить пользователя')

