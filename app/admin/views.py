from flask import render_template, request
from app.func import login_required
from app.admin.func import create_user
from app.admin.forms import AddUserForm

@login_required
def create_usr():
    form = AddUserForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        print('post')
        req = create_user()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('addusr.html', form=form,  
                               title='Добавить пользователя')

