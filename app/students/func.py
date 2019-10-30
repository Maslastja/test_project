import peewee as pw
from flask import request
from datetime import date
from app.models.group import Group
from app.models.student import Student


    
# добавление нового студента
def add_student(stinfo):
    gr = Group.get_by_id(stinfo['group'])
    stud = Student.select().where(Student.surname == stinfo['surname'],
                                  Student.firstname == stinfo['firstname'],
                                  Student.secondname == stinfo['secondname'],
                                  Student.birthdate == stinfo['birthdate'],
                                  Student.numticket == stinfo['numticket'])
    if len(stud) == 0:
        row = Student(
            surname=stinfo['surname'],
            firstname=stinfo['firstname'],
            secondname=stinfo['secondname'],
            birthdate=stinfo['birthdate'],
            numticket=stinfo['numticket'],
            group=gr
        )
        row.save()
        req = f'Создан студент {stinfo["surname"]} {stinfo["firstname"]} ' 
        f'{stinfo["secondname"]}, дата рождения {stinfo["birthdate"]}, '
        f'№ студбилета {stinfo["numticket"]}, группа {str(gr)}'
    else:
        req = f'Студент {stinfo["surname"]} {stinfo["firstname"]} '
        f'{stinfo["secondname"]} уже создан'
        
    return req

# возврат всего списка студентов
def find_all_students():
    arg_id = request.args.get('id')
    arg_gr = request.args.get('group')
    sel = (Student.select(
        Student,
        Group.groupname)
        .join(Group, pw.JOIN.LEFT_OUTER, on=(Student.group_id == Group.id))
        .order_by(Group.groupname, 
                  Student.surname, 
                  Student.firstname, 
                  Student.secondname))
        
    if arg_id:
        sel = sel.where(Student.id == arg_id)
    if arg_gr:
        sel = sel.where(Group.groupname == str(arg_gr))
    
    stud = []
    i=1
    for student in sel.namedtuples():
        #print(student)
        stud.append(
            {'id': student.id,
             'ind': i,
             'idradio': f'radio-{i-1}',
             'f': f'{student.surname} {student.firstname} {student.secondname}',
             'bdate': f'{student.birthdate:%Y-%m-%d}',
             't': student.numticket,
             'gr': student.groupname
            })
        i=i+1
    
    return stud

# удаление студента
def delete_stud(id):
    stud = Student.get_by_id(id)
    oldname = str(stud)
    gr_with_stud = Group.get_by_stud(stud)
    if len(gr_with_stud) == 0:
        result = Student.delete_by_id(id)
        if result != 0:
            req = f'студент {oldname} успешно удален'
    else:
        for g in gr_with_stud:
            gname = g.groupname
        req = f'Невозможно удалить студента т.к. он староста в группе {gname}'
            
    return req

# обновление информации студента
def update_stud(stud, stinfo):
                                            
    oldfio = str(stud)
    if (stinfo['surname'] == stud.surname and 
        stinfo['firstname'] == stud.firstname and 
        stinfo['secondname'] == stud.secondname and
        stinfo['birthdate'] == stud.birthdate and 
        stinfo['numticket'] == stud.numticket and 
        stinfo['group'] == stud.group.id):
        req = 'нечего изменять'
    else:                    
        if stinfo['surname'] != stud.surname:
            stud.surname = stinfo['surname']
        if stinfo['firstname'] != stud.firstname:
            stud.firstname = stinfo['firstname']
        if stinfo['secondname'] != stud.secondname:
            stud.secondname = stinfo['secondname']
        if stinfo['birthdate'] != stud.birthdate:
            stud.birthdate = stinfo['birthdate']
        if stinfo['numticket'] != stud.numticket:
            stud.numticket = stinfo['numticket']
        str_star=''
        if stinfo['group'] != stud.group.id:
            gr = Group.get_by_id(stinfo['group'])
            if gr is not None:
                if stud == stud.group.starosta and gr != stud.group:
                    str_star = ' невозможно изменить группу, т.к. '
                    'студент является старостой'
                else:
                    stud.group = gr
        stud.save()
        req = (f'Студент {oldfio} успешно обновлен ' +
                (f'{str_star}' if str_star != '' else ''))
        
    return req
