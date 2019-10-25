import peewee as pw
import playhouse.flask_utils as ph
from config.database import db

class Student(db.Model):
    id = pw.PrimaryKeyField(null=False)
    surname = pw.CharField(max_length=50, null=False)
    firstname = pw.CharField(max_length=50, null=False)
    secondname = pw.CharField(max_length=50)
    birthdate = pw.DateField()
    numticket = pw.IntegerField()
    group = pw.DeferredForeignKey('Group', null=True)

    class Meta:
        db_table = "students"
        order_by = ('id',)

    def __str__(self):
        return f'{self.surname} {self.firstname} {self.secondname}'
     
    # удаление студента по id
    def del_stud(id):
        stud = Student.delete().where(Student.id == id).execute()
        return stud
 
    # возврат списка выбора студентов (кортеж)
    def stud_select(gr=None):
        stud = [(0, 'не указан')]
        if gr is not None:
            sel = (Student.select(Student)
                   .where(Student.group_id == gr))
        else:
            sel = Student.select(Student)
       
        for st in sel:
            stud.append((st.id,f'{st.surname} {st.firstname} {st.secondname} '
            f', {str(st.group)}'))
        
        return stud

