from flask import request, render_template
from app.func import gr_select, stud_select, login_required
from app.students.func import (find_all_students, add_student, 
                          delete_stud, update_stud, stud_fio)
from app.students.forms import AddStudentForm, UpStudentForm,  DelStudentForm

#@bp.route('/student')
@login_required
def get_students():
    students = find_all_students()
    stud = []
    i=1
    for student in students:
        stud.append(
            {'ind': i,
             'f': stud_fio(student),
             'bdate': f'{student.birthdate:%Y-%m-%d}',
             't': student.numticket,
             'gr': student.groupname
             })
        i=i+1
    return render_template('student.html', stud=stud,  
                               title='Список студентов')


#@bp.route('/addstudent', methods=['GET', 'POST'])
@login_required
def addstudent():
    gr = gr_select()
    form = AddStudentForm()
    form.name.choices = gr
    
    if request.method == 'POST' and form.validate_on_submit():
        req = add_student()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('addstudent.html', form=form, 
                               title='Добавить студента')

#@bp.route('/delstudent', methods=['GET', 'POST'])
@login_required
def delstudent():
    stud = stud_select()
    form = DelStudentForm()
    form.id.choices = stud
    
    if request.method == 'POST' and form.validate_on_submit():
        req = delete_stud()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('delstudent.html', form=form,  
                               title='Удалить студента')

#@bp.route('/upstudent', methods=['GET', 'POST'])
@login_required
def upstudent():
    gr = gr_select()
    stud = stud_select()
    form = UpStudentForm()
    form.gr_id.choices = gr
    form.id.choices = stud
    
    if request.method == 'POST' and form.validate_on_submit():
        req = update_stud()
        return render_template('req.html', req=req, title='Группы и студенты')
    else:    
        return render_template('upstudent.html', form=form,  
                               title='Изменить студента')
