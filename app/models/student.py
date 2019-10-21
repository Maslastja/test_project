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
        return (f'{self.surname} {self.firstname} {self.secondname}')
    
    # поиск студента по id
    def get_by_id(id):
        stud = ph.get_object_or_404(Student, Student.id == id)
        #print(stud)
        return stud
    
    # удаление студента по id
    def del_stud(id):
        stud = Student.delete().where(Student.id == id).execute()
        return stud
 
    # возврат списка выбора студентов (кортеж)
    def stud_select():
        sel = (Student.select(Student))
        
        stud = [(0, 'не указан')]
        for st in sel:
            stud.append((st.id,(f'{st.surname} {st.firstname} {st.secondname} \
            , {str(st.group)}')))
        
        return stud

    # выборка студентов в группе
    def stud_in_group(gr):
        sel = Student.select().where(Student.group == gr)
        
        return stud
