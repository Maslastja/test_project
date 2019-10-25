from flask import (Blueprint, request, render_template, redirect, session, 
                   make_response)
from app.forms import LoginForm
from app.func import check_logpass, login_required

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg=''
    if request.method == 'POST' and form.validate_on_submit():
        usr = check_logpass()
        user = usr[0]
        if user is not None:
            next_page = request.args.get('next')
            if not next_page:
                resp = redirect('/index')
                #print(resp)
            else:
                resp = redirect(next_page) 
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['isadmin'] = user.isadmin
            return resp
        else:
            msg = f'{usr[1]}. Повторите попытку.'
        
    resp = make_response(render_template('login.html', form=form, 
                                             title='Вход', msg=msg))
    
    return resp

@bp.route('/logout')
@login_required
def logout():
    #выход пользователя, обнулить запомненный id пользователя
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('isadmin', None)
    resp = redirect('/login')
    
    return resp


