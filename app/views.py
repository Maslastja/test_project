from flask import request, render_template, redirect, session, make_response
from app.forms import LoginForm
from app.func import check_logpass, login_required

#@app.route('/index')
@login_required
def index():
    #if 'user_id' in session:
        #print(session['user_id'])
    #else:
        #print('no')
    return render_template('index.html', title='Группы и студенты')

def login():
    #выход пользователя, обнулить запомненный id пользователя
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('isadmin', None)
    form = LoginForm()
    msg=''
    if request.method == 'POST' and form.validate_on_submit():
        usr = check_logpass()
        user = usr[0]
        if user is not None:
            #login_user(user)
            next_page = request.args.get('next')
            if not next_page:
                resp = redirect('/index')
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
