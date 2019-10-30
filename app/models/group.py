import peewee as pw
import playhouse.flask_utils as ph
from config.database import db
from app.models.student import Student

class Group(db.Model):
    id = pw.PrimaryKeyField(null=False)
    groupname = pw.CharField(max_length=150)
    starosta = pw.ForeignKeyField(Student, null=True)
    class Meta:
        db_table = "groups"
        order_by = ('id',)

    def __str__(self):
        return self.groupname
            
    #поиск группы по старосте
    def get_by_stud(stud):
        #не использован метод get_object_or_404 т.к. нет необходимости получить
        #именно объект
        gr_with_stud = (Group
                        .select()
                        .where(Group.starosta == stud)
                        .namedtuples())
        return gr_with_stud

    # возврат списка выбора групп (кортеж)
    def gr_select():
        sel = (Group
              .select(
              Group.groupname,
              Group.id)
              .namedtuples())
        
        gr = [(0, 'не указана')]
        for group in sel:
            gr.append((group.id,group.groupname))
        
        return gr
