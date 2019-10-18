from flask import render_template, request, make_response
from app.models.group import Group
from app.models.student import Student
from app.groups.func import (find_all_groups, add_group, 
                          update_group, delete_group)
from app.groups.forms import AddGroupForm, UpGroupForm, DelGroupForm
from secretary import Renderer
import subprocess

def add_group_form():
    form = AddGroupForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        req = add_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('addgroup.html', form=form,  
                               title='Добавить группу')
    
def get_groups():
    gr = find_all_groups()
    return render_template('group.html', gr=gr,  
                               title='Список групп')

def upgroup():
    gr = Group.gr_select()
    stud = Student.stud_select()
    form = UpGroupForm()
    form.id.choices = gr
    form.stud_id.choices = stud
      
    if request.method == 'POST' and form.validate_on_submit():
        req = update_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('upgroup.html', form=form,  
                               title='Изменить группу')

def delgroup():
    gr = Group.gr_select()
    form = DelGroupForm()
    form.id.choices = gr
    
    if request.method == 'POST' and form.validate_on_submit():
        req = delete_group()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('delgroup.html', form=form,  
                               title='Удалить группу')
def test_secr():
    engine = Renderer()
    template = open('app/groups/template.odt', 'rb')
    output = open('output.odt', 'wb')
    eng = engine.render(template, image='app/groups/writer.png')
    output.write(eng)
    p = subprocess.call(['unoconv', '-f', 'pdf', 'output.odt'])
    with open('output.pdf', 'rb') as f:
        file_content = f.read()
    
    response = make_response(file_content, 200)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
                'inline'
    #response.headers['Content-Disposition'] = \
                #'inline; filename=output.pdf'
    return response    
     #return ("Template rendering finished! Check output.odt file.")
