from flask import request, render_template
from app.models.group import Group
from app.models.student import Student
from app.students.func import (find_all_students, add_student, 
                          delete_stud, update_stud)
from app.students.forms import AddStudentForm, UpStudentForm,  DelStudentForm

def get_students():
    stud = find_all_students()
    return render_template('student.html', stud=stud,  
                               title='Список студентов')

def addstudent():
    gr = Group.gr_select()
    form = AddStudentForm()
    form.gr_id.choices = gr
    
    if request.method == 'POST' and form.validate_on_submit():
        req = add_student()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        elsereq = render_template('addstudent.html', form=form, 
                                       title='Добавить студента')
        return elsereq

def delstudent():
    stud = Student.stud_select()
    form = DelStudentForm()
    form.id.choices = stud
    
    if request.method == 'POST' and form.validate_on_submit():
        req = delete_stud()    
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        elsereq = render_template('delstudent.html', form=form,  
                                       title='Удалить студента')
        return elsereq

def upstudent():
    gr = Group.gr_select()
    stud = Student.stud_select()
    form = UpStudentForm()
    form.gr_id.choices = gr
    form.id.choices = stud
    
    if request.method == 'POST' and form.validate_on_submit():
        req = update_stud()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        elsereq = render_template('upstudent.html', form=form,  
                               title='Изменить студента')
        return elsereq

