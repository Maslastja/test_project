from flask import render_template, request, flash
from app.admin.forms import AddUserForm
from app.models.users import User

def create_usr():
    form = AddUserForm(request.form or None)
    if request.method == 'POST' and form.validate():
        u = User(username=form.username.data,
                 pwd=form.password.data)
        u.save()
        if u is not None:
            req = f'Создан пользователь {form.username.data}'
            flash(req)            form = AddUserForm() #переопределение формы, чтобы поля были пустыми
    
    return render_template('addusr.html', form=form,  
                               title='Добавить пользователя')

