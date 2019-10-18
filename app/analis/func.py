import peewee as pw
from app.models.group import Group
from app.models.student import Student

# вывод информации о количестве студентов в группе
def analis_gr():
    g = Group.alias()
    s = Student.alias()
    s1 = Student.alias()
    sel = (g
           .select(
               g.groupname,
               pw.fn.Count(s.id).alias('count'),
               pw.fn.Max(pw.fn.CONCAT_WS(' ',
                                   s1.surname,
                                   s1.firstname,
                                   s1.secondname)).alias('fio'))
           .join(s, pw.JOIN.LEFT_OUTER, on=(s.group_id == g.id))
           .join(s1, pw.JOIN.LEFT_OUTER, on=(s1.id == g.starosta_id))
           .group_by(g.groupname).having(pw.fn.Count(s.id)>0)
           .namedtuples())

    req = []
    for stroka in sel:
        req.append( 
            {'grname': stroka.groupname,
             'count': stroka.count,
             'star': (stroka.fio if stroka.fio != '' else 'не указан')
             }
        )
    return req
