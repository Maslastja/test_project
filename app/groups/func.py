import peewee as pw
from flask import request
from datetime import date
from app.models.group import Group
from app.models.student import Student

# возврат полного ФИО студента
def stud_fio(stud):
    return f'{stud.surname} {stud.firstname} {stud.secondname}'

# добавление новой группы
def add_group():
    name = request.form.get('name')
    gr = Group.select().where(Group.groupname == name)
    if len(gr) == 0:
        row = Group(
            groupname=name
            #starosta=stud
        )
        row.save()
        req = (f'Создана группа {name}')
        return req
    else:
        req = (f'Группа {name} уже создана')
    
    return req

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

# удаление группы по наименованию
def delete_group():
    id = int(request.form.get('id'))
    if id:
        gr = search_gr_by_id(id)
        #if len(gr) == 0:
        if gr is None:
            req = (f'Группы с id {id} не существует')
        else:
            oldname = gr.groupname
            stud_with_gr = Student.select().where(Student.group == gr)
            if len(stud_with_gr) == 0:
                gr = Group.delete().where(Group.id == gr.id).execute()
                req = f'группа {oldname} успешно удалена'
            else:
                req = 'Невозможно удалить группу т.к. в ней есть студенты: '
                for s in stud_with_gr:
                    req = req + stud_fio(s) + ' '
    else:
        req = 'не указан id группы для удаления'
    
    return req

# обновление информации группы
def update_group():
    id = int(request.form.get('id'))
    gr = search_gr_by_id(id)
    if gr is not None:
        name = request.form.get('name')
        stud_id = request.form.get('stud_id')
        if name == '' and (stud_id == '' or stud_id != 0):
            req = 'нечего изменять'
        else:
            if stud_id != '':
                stud = search_stud_by_id(int(stud_id))
            else:
                stud = None
            
            str_star = ''
            if stud is not None:
                if stud.group != gr:
                    str_star = (f' студент {stud_fio(stud)} не задан старостой \
                    т.к. находится в другой группе')
                    stud = None
                    if name == '':
                        return (f'нечего изменять, {str_star}')
            else:
                str_star = f' староста по id {stud_id} не найден'
            oldname = gr.groupname
            if name != '':
                gr.groupname = name
            if stud != None:
                gr.starosta = stud
            gr.save()
            req = ((f'Группа {oldname} успешно обновлена')+  
            (f'{str_star}' if str_star != '' else ''))
    else:
        req = 'группа не найдена!'

    return req
# возврат всего списка групп
def find_all_groups():
    
    sel = (Group
          .select(
          Group.groupname,
          Group.id,
          pw.fn.concat_ws(' ',Student.surname,
                          Student.firstname,
                          Student.secondname)
          .alias('fio'))
          .join(Student, pw.JOIN.LEFT_OUTER, 
                on=(Student.id == Group.starosta_id))
          .order_by(Group.groupname)
          .namedtuples())
    
    return sel                

# поиск студента по id
def search_stud_by_id(id):
    stud = (Student
            .select()
            .where(Student.id == id))
    
    if len(stud) == 0:
        return None
    else:
        return stud.get()

            

