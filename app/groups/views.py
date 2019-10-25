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
    #print(url_for('.groupform'))
    if request.method == 'POST':
        if 'addsub' in request.form:
            resp = redirect(url_for('.groupform'))
        if 'testdoc' in request.form:
            resp = redirect(url_for('.test_secr'))
        elif 'radio' in request.form:
            if 'changesub' in request.form:
                resp = redirect(url_for('.groupform', id=request.form['radio']))
            elif 'delsub' in request.form:
                resp = redirect(url_for('.delgroup', id=request.form['radio']))
    return resp

def groupform():
    arg_id = request.args.get('id')
    if arg_id is not None:
        group = Group.get_by_id(arg_id)
        form = GroupForm(obj=group)
        stud = Student.stud_select(arg_id)
        form.star.choices = stud
        if group.starosta is not None:
            form.star.data = group.starosta.id
        title = 'Изменить группу'
    else:
        group = None
        form = GroupForm()
        #без этого не отрабатывала валидация. ругалость, что не выбран староста
        form.star.choices = [(0,'')]
        form.star.data = 0
        #
        title = 'Добавить группу'
    
    if request.method == 'POST' and form.validate_on_submit():
        if arg_id is not None:
            req = update_group(group)
        else:
            req = add_group()
        flash(req)
        return redirect(url_for('.get_groups'))
    else:
        return render_template('groupform.html', group=group, 
                    form=form, title=title)

def delgroup():
    arg_id = request.args.get('id')
    req = delete_group(arg_id)
    flash(req)
    return redirect(url_for('.get_groups'))

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

