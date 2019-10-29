import peewee as pw
from flask import request
from datetime import date
from app.models.group import Group
from app.models.student import Student

# добавление новой группы
def add_group():
    name = request.form.get('groupname')
    gr = Group.select().where(Group.groupname == name)
    if len(gr) == 0:
        row = Group(
            groupname=name
        )
        row.save()
        req = (f'Создана группа {name}')
        return req
    else:
        req = (f'Группа {name} уже создана')
    
    return req

# удаление группы 
def delete_group(arg_id):
    gr = Group.get_by_id(arg_id)
    oldname = gr.groupname
    stud_in_gr = Student.stud_select(arg_id)
    if len(stud_in_gr) == 1 and stud_in_gr[0][0]==0:
        result = Group.del_gr(arg_id)
        if result != 0:
            req = f'группа {oldname} успешно удалена'
    else:
        req = 'Невозможно удалить группу т.к. в ней есть студенты: '
        st = ''
        for s in stud_in_gr:
            if s[0] != 0:
                st=f'{st} {s[1]}; '
        req = f'{req} {st} '
    return req

# обновление информации группы
def update_group(gr):
    if gr is not None:
        name = request.form.get('groupname')
        stud_id = int(request.form.get('star'))
        if name == gr.groupname and ((gr.starosta is None and stud_id == 0) or 
                                     (gr.starosta is not None and 
                                      stud_id == gr.starosta.id)):
            req = 'нечего изменять'
        else:
            if stud_id != 0:
                stud = Student.get_by_id(stud_id)
            else:
                stud = None
            
            str_star = ''
            if stud is not None:
                if stud.group != gr:
                    str_star = (f' студент {str(stud)} не задан старостой \
                    т.к. находится в другой группе')
                    stud = None
                    if name == '':
                        return (f'нечего изменять, {str_star}')
            else:
                str_star = f' староста по id {stud_id} не найден'
            oldname = str(gr)
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
    
    gr = []
    i=1
    for group in sel:
        gr.append(
            {'id': group.id,
             'ind':i,
             'idradio': f'radio-{i-1}',
             'grname': group.groupname,
             'star': f'{group.fio}' if group.fio != '' else 'не указан'
             }
        )
        i=i+1

    return gr 