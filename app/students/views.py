from flask import request, render_template, redirect, url_for, flash
from app.models.group import Group
from app.models.student import Student
from app.students.func import (find_all_students, add_student, 
                          delete_stud, update_stud)
from app.students.forms import StudentForm, ListStudentForm

def get_students():
    stud = find_all_students()
    students = []
    for ind in stud:
        students.append((ind['id'], ind['idradio']))
    form = ListStudentForm()
    form.radio.choices = students
    resp = render_template('student.html', stud=stud, form=form, 
                               title='Список студентов')
    if request.method == 'POST':
        if 'addsub' in request.form:
            resp = redirect(url_for('students.studentform'))
        elif 'radio' in request.form:
            id=request.form['radio']
            if 'changesub' in request.form:
                resp = redirect(url_for('students.studentform', id=id))
            elif 'delsub' in request.form:
                resp = redirect(url_for('students.delstudent', id=id))
    return resp

def delstudent():
    arg_id = request.args.get('id')
    req = delete_stud(arg_id)    
    flash(req)
    return redirect(url_for('students.get_students'))

def studentform():
    gr = Group.gr_select()
    arg_id = request.args.get('id')
    if arg_id is not None:
        stud = Student.get_by_id(arg_id)
        form = StudentForm(request.form or None, obj=stud)
        form.group.choices = gr
        form.group.data = stud.group.id
    else:
        form = StudentForm(request.form or None)
        form.group.choices = gr
    
    if request.method == 'POST' and form.validate():
        studinfo = get_stud_info(form)
        if arg_id is not None:
            req = update_stud(stud, studinfo)
        else:
            req = add_student(studinfo)
        flash(req)
        return redirect(url_for('students.get_students'))
    else:    
        elsereq = render_template('studentform.html', form=form,  
                               title='Изменить студента')
        return elsereq

# получить информацию для функций
def get_stud_info(form):
    studinfo={
        'surname': form.surname.data,
        'firstname': form.firstname.data,
        'secondname': form.secondname.data,
        'birthdate': form.birthdate.data,
        'numticket': form.numticket.data,
        'group': int(request.form['group']) #из form.group.data не берет знач.
    }
    
    return studinfo
