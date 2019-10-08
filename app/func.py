import peewee as pw
from flask import request, session, redirect, url_for
from functools import wraps
from werkzeug.security import check_password_hash
from datetime import date
from app.models.group import Group
from app.models.student import Student
from app.models.users import User

# возврат полного ФИО студента
def stud_fio(stud):
    return f'{stud.surname} {stud.firstname} {stud.secondname}'

# возврат списка выбора групп (кортеж)
def gr_select():
    sel = (Group
          .select(
          Group.groupname,
          Group.id)
          .namedtuples())
    
    gr = [(0, 'не указана')]
    for group in sel:
        gr.append((group.id,group.groupname))
    
    return gr
 
# возврат списка выбора студентов (кортеж)
def stud_select():
    sel = (Student.select(
        Student,
        Group.groupname)
        .join(Group, pw.JOIN.LEFT_OUTER, on=(Student.group_id == Group.id))
        .namedtuples())
    
    stud = [(0, 'не указан')]
    for st in sel:
        stud.append((st.id,(f'{st.surname} {st.firstname} {st.secondname},\
        {st.groupname}')))
    
    return stud
 
# возврат соответствия логина и пароля
def check_logpass():
    username = request.form.get('username')
    password = request.form.get('password')
    #sel = (User.select()
           #.where(User.username == username))
    sel = User.sel_user_by_name(username)
    
    if len(sel) == 0:
        return (None, 'Неверный логин')
    else:
        usr = sel.get()
        if check_password_hash(usr.password, password):
            return (usr, '')
        else:
            return (None, 'Неверный пароль')

#декоратор ограничения использования функций только авториз. пользователей
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

