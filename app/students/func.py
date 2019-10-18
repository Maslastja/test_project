import peewee as pw
from flask import request
from datetime import date
from app.models.group import Group
from app.models.student import Student


# получить информацию из запроса
def get_stud_info():
    studinfo={
        'f': request.form.get('f'),
        'i': request.form.get('i'),
        'o': request.form.get('o'),
        'bdate': request.form.get('bdate'),
        't': request.form.get('t'),
        'gr_id': request.form.get('gr_id')
    }
    
    return studinfo
    
# добавление нового студента
def add_student():
    stinfo = get_stud_info()
    gr = Group.get_by_id(stinfo['gr_id'])
    bdar = stinfo['bdate'].split('.')
    stud = Student.select().where(Student.surname == stinfo['f'],
                                  Student.firstname == stinfo['i'],
                                  Student.secondname == stinfo['o'],
                                  Student.birthdate == date(int(bdar[2]),
                                                            int(bdar[1]),
                                                            int(bdar[0])),
                                  Student.numticket == stinfo['t'])
    if len(stud) == 0:
        bd = bdar[2] + '-' + bdar[1] + '-' + bdar[0]
        row = Student(
            surname=stinfo['f'],
            firstname=stinfo['i'],
            secondname=stinfo['o'],
            birthdate=bd,
            numticket=stinfo['t'],
            group=gr
        )
        row.save()
        req = (f'Создан студент {stinfo["f"]} {stinfo["i"]} {stinfo["o"]}, \
        дата рождения {stinfo["bdate"]}, № студбилета {stinfo["t"]}, \
        группа {gr.groupname}')
    else:
        req = (f'Студент {stinfo["f"]} {stinfo["i"]} {stinfo["o"]} уже создан')
        
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
             'f': f'{student.surname} {student.firstname} {student.secondname}',
             'bdate': f'{student.birthdate:%Y-%m-%d}',
             't': student.numticket,
             'gr': student.groupname
            })
        i=i+1
    
    return stud

# удаление студента
def delete_stud():
    id = request.form.get('id')
    if id:
        stud = Student.get_by_id(id)
        oldname = str(stud)
        gr_with_stud = Group.get_by_stud(stud)
        if len(gr_with_stud) == 0:
            result = Student.del_stud(id)
            if result != 0:
                req = (f'студент {oldname} успешно удален')
        else:
            for g in gr_with_stud:
                gname = g.groupname
            req = (f'Невозможно удалить студента т.к. он староста в группе\
                  {gname}') 
            
        return req

# обновление информации студента
def update_stud():
    id = request.form.get('id')
    if id:
        stud = Student.get_by_id(id)
        print(stud)
        if stud is not None:
            stinfo = get_stud_info()
            print(stinfo)
                                            
            oldfio = str(stud)
            if (stinfo['f'] == '' and stinfo['i'] == '' and 
                stinfo['o'] == '' and stinfo['bdate'] == '' and 
                stinfo['t'] == '' and stinfo['gr_id'] == '0'):
                req = 'нечего изменять'
            else:    
                if stinfo['f'] != '':
                    stud.surname = stinfo['f']
                if stinfo['i'] != '':
                    stud.firstname = stinfo['i']
                if stinfo['o'] != '':
                    stud.secondname = stinfo['o']
                if stinfo['bdate'] != '':
                    bdar = stinfo['bdate'].split('.')
                    stud.birthdate = bdar[2] + '-' + bdar[1] + '-' + bdar[0]
                if stinfo['t'] != '':
                    stud.numticket = stinfo['t']
                str_star=''
                if stinfo['gr_id'] != '0':
                    gr = Group.get_by_id(stinfo['gr_id'])
                    if gr is not None:
                        if stud == stud.group.starosta and gr != stud.group:
                            str_star = ' невозможно изменить группу, т.к. \
                            студент является старостой'
                        else:
                            stud.group = gr
                stud.save()
                req = ((f'Студент {oldfio} успешно обновлен')+
                       (f'{str_star}' if str_star != '' else ''))
        else:
            req = f'студент по id {id} не найден'
            
        return req
