import peewee as pw
from flask import request
from datetime import date
from app.models.group import Group
from app.models.student import Student

# возврат полного ФИО студента
def stud_fio(stud):
    return f'{stud.surname} {stud.firstname} {stud.secondname}'

# поиск группы по наименованию
def search_gr(name):
    gr = Group.select().where(Group.groupname == name)
    if len(gr) == 0:
        print(f'Группы {name} не существует')
        return None
    else:
        return gr.get()

# поиск группы по id
def search_gr_by_id(id):
    gr = Group.select().where(Group.id == id)
    if len(gr) == 0:
        return None
    else:
        return gr.get()

# добавление нового студента
def add_student():
    f = request.form.get('f')
    i = request.form.get('i')
    o = request.form.get('o')
    bdate = request.form.get('bdate')
    t = int(request.form.get('t'))
    name = request.form.get('name')
    gr = search_gr_by_id(int(name))
    bdar = bdate.split('.')
    stud = Student.select().where(Student.surname == f,
                                  Student.firstname == i,
                                  Student.secondname == o,
                                  Student.birthdate == date(int(bdar[2]),
                                                            int(bdar[1]),
                                                            int(bdar[0])),
                                  Student.numticket == t)
    if len(stud) == 0:
        bd = bdar[2] + '-' + bdar[1] + '-' + bdar[0]
        row = Student(
            surname=f,
            firstname=i,
            secondname=o,
            birthdate=bd,
            numticket=t,
            group=gr
        )
        row.save()
        req = (f'Создан студент {f} {i} {o}, дата рождения {bdate}, № студбилета'
             f' {t}, группа {gr.groupname}')
    else:
        req = (f'Студент {f} {i} {o} уже создан')
        
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
    
    return sel.namedtuples()

# поиск студента по id
def search_stud_by_id(id):
    stud = (Student
            .select()
            .where(Student.id == id))
    
    if len(stud) == 0:
        return None
    else:
        return stud.get()

# поиск студента по ФИО
def search_stud(f, i, o):
    stud = (Student
            .select()
            .where(Student.surname == f,
                   Student.firstname == i,
                   Student.secondname == o)
            )
    
    if len(stud) == 0:
        print(f'Студента  {f} {i} {o} не существует')
        return None
    else:
        return stud.get()

# удаление студента по номеру студенческого билета
def delete_stud():
    id = request.form.get('id')
    if id:
        stud = Student.select().where(Student.id == id)
        if len(stud) == 0:
            req = (f'Студента с id {id} не существует')
        else:
            stud = stud.get()
            oldname = stud_fio(stud)
            gr_with_stud = (Group
                            .select()
                            .where(Group.starosta == stud)
                            .namedtuples())
            if len(gr_with_stud) == 0:
                stud = Student.delete().where(Student.id == id).execute()
                if stud != 0:
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
        stud = search_stud_by_id(id)
        if stud is not None:
            f = request.form.get('f')
            i = request.form.get('i')
            o = request.form.get('o')
            bdate = request.form.get('bdate')
            t = request.form.get('t')
            gr_id = request.form.get('gr_id')
                                
            oldfio = stud_fio(stud)
            if (f == '' and i == '' and o == '' and bdate == '' and t == '' and 
            gr_id == ''):
                req = 'нечего изменять'
            else:    
                if f != '':
                    stud.surname = f
                if i != '':
                    stud.firstname = i
                if o != '':
                    stud.secondname = o
                if bdate != '':
                    bdar = bdate.split('.')
                    stud.birthdate = bdar[2] + '-' + bdar[1] + '-' + bdar[0]
                if t != '':
                    stud.numticket = int(t)
                str_star=''
                if gr_id != '':
                    gr = search_gr_by_id(gr_id)
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
