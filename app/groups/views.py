from flask import render_template, request, make_response
from app.func import gr_select, stud_select, login_required
from app.groups.func import (find_all_groups, add_group, 
                          update_group, delete_group)
from app.groups.forms import AddGroupForm, UpGroupForm, DelGroupForm


#@bp.route('/addgroup', methods=['GET', 'POST'])
@login_required
def add_group_form():
    form = AddGroupForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        req = add_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('addgroup.html', form=form,  
                               title='Добавить группу')
    
#@bp.route('/group')
@login_required
def get_groups():
    groups = find_all_groups()
    gr = []
    i=1
    for group in groups:
        gr.append(
            {'ind':i,
             'grname': group.groupname,
             'star': (f'{group.fio}' if group.fio != '' else 'не указан')
             }
        )
        i=i+1
    
    return render_template('group.html', gr=gr,  
                               title='Список групп')

#@bp.route('/upgroup', methods=['GET', 'POST'])
@login_required
def upgroup():
    gr = gr_select()
    stud = stud_select()
    form = UpGroupForm()
    form.id.choices = gr
    #form.stud_id.data = 0 
    form.stud_id.choices = stud
      
    if request.method == 'POST' and form.validate_on_submit():
        req = update_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('upgroup.html', form=form,  
                               title='Изменить группу')

#@bp.route('/delgroup', methods=['GET', 'POST'])
@login_required
def delgroup():
    gr = gr_select()
    form = DelGroupForm()
    form.id.choices = gr
    
    if request.method == 'POST' and form.validate_on_submit():
        req = delete_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('delgroup.html', form=form,  
                               title='Удалить группу')

