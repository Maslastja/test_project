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
            resp = redirect(url_for('.studentform'))
        elif 'radio' in request.form:
            if 'changesub' in request.form:
                resp = redirect(url_for('.studentform', id=request.form['radio']))
            elif 'delsub' in request.form:
                resp = redirect(url_for('.delstudent', id=request.form['radio']))
    return resp

def delstudent():
    arg_id = request.args.get('id')
    req = delete_stud(arg_id)    
    flash(req)
    return redirect(url_for('.get_students'))

def studentform():
    gr = Group.gr_select()
    arg_id = request.args.get('id')
    if arg_id is not None:
        stud = Student.get_by_id(arg_id)
        form = StudentForm(obj=stud)
        form.group.choices = gr
        form.group.data = stud.group.id
    else:
        form = StudentForm()
        form.group.choices = gr
    
    if request.method == 'POST' and form.validate_on_submit():
        if arg_id is not None:
            req = update_stud(stud)
        else:
            req = add_student()
        flash(req)
        return redirect(url_for('.get_students'))
    else:    
        elsereq = render_template('studentform.html', form=form,  
                               title='Изменить студента')
        return elsereq

