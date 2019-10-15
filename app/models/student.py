import peewee as pw
#from app.models.group import Group
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