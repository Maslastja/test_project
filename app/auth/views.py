from flask import request, render_template, redirect, session, make_response, url_for
from .forms import LoginForm
from app.func import login_required
from app.models.users import User

def login():
    form = LoginForm(request.form or None)
    if request.method == 'POST' and form.validate():
        user = (User.select()
                .where(User.username == request.form.get('username')).get())
        next_page = request.args.get('next')
        if not next_page:
            resp = redirect('/index')
        else:
            resp = redirect(next_page) 
            
        session['user_id'] = user.id
        session['username'] = user.username
        session['isadmin'] = user.isadmin
        return resp
            
    resp = render_template('login.html', form=form, title='Вход')
    
    return resp

@login_required
def logout():
    #выход пользователя, обнулить запомненный id пользователя
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('isadmin', None)
    resp = redirect('/login')
    
    return resp

