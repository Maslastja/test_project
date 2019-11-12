from flask import (render_template, request, make_response, redirect, url_for, 
                   flash)
from app.models.group import Group
from app.models.student import Student
from app.groups.func import (find_all_groups, add_group, 
                             update_group, delete_group)
from app.groups.forms import ListGroupForm, GroupForm
from secretary import Renderer

def get_groups():
   
    gr = find_all_groups()
    groups = []
    for ind in gr:
        groups.append((ind['id'], ind['idradio']))
    form = ListGroupForm()
    form.radio.choices = groups
    resp = render_template('group.html', gr=gr, form=form, 
                                           title='Список групп')
    if request.method == 'POST':
        if 'addsub' in request.form:
            resp = redirect(url_for('groups.groupform'))
        if 'testdoc' in request.form:
            resp = redirect(url_for('groups.test_secr'))
        elif 'radio' in request.form:
            id=request.form['radio']
            if 'changesub' in request.form:
                resp = redirect(url_for('groups.groupform', id=id))
            elif 'delsub' in request.form:
                resp = redirect(url_for('groups.delgroup', id=id))
    return resp

def groupform():
    arg_id = request.args.get('id')
    if arg_id is not None:
        group = Group.get_by_id(arg_id)
        form = GroupForm(request.form or None, obj=group)
        stud = Student.stud_select(arg_id)
        form.star.choices = stud
        if group.starosta is not None:
            form.star.data = group.starosta.id
        else:
            form.star.data = 0
        title = 'Изменить группу'
    else:
        group = None
        form = GroupForm(request.form or None)
        #без этого не отрабатывала валидация. ругалость, что не выбран староста
        form.star.choices = [(0,'')]
        form.star.data = 0
        #
        title = 'Добавить группу'
    
    if request.method == 'POST' and form.validate():
        if arg_id is not None:
            req = update_group(group, form.groupname.data, form.star.data)
        else:
            req = add_group(form.groupname.data)
        flash(req)
        return redirect(url_for('groups.get_groups'))
    else:
        return render_template('groupform.html', group=group, 
                    form=form, title=title)

def delgroup():
    arg_id = request.args.get('id')
    req = delete_group(arg_id)
    flash(req)
    return redirect(url_for('groups.get_groups'))

def test_secr():
    gr = find_all_groups()
    engine = Renderer()
    template = open('app/groups/templates/template.odt', 'rb')
    eng = engine.render(template, image='app/groups/writer.png', stroki=gr)
    #eng возвращает двоичный объект - заполненный шаблон
    response = make_response(eng)
    response.headers['Content-Type'] = 'application/vnd.oasis.opendocument.text'
    response.headers['Content-Disposition'] = \
                'attachment; filename=testfile.odt'
    return response    

