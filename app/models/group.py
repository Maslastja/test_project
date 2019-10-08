import peewee as pw
from config.database import db

class Group(db.Model):
    id = pw.PrimaryKeyField(null=False)
    groupname = pw.CharField(max_length=150)
    starosta = pw.DeferredForeignKey('Student', null=True)
    class Meta:
        db_table = "groups"
        order_by = ('id',)