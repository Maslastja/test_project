import peewee as pw
from config.database import db
from app.models.student import Student

class Group(db.Model):
    id = pw.PrimaryKeyField(null=False)
    groupname = pw.CharField(max_length=150)
    starosta = pw.ForeignKeyField(Student)
    class Meta:
        db_table = "groups"
        order_by = ('id',)