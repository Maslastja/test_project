import peewee as pw
from config.database import db

class User(db.Model):
       id = pw.PrimaryKeyField(null=False)
       username = pw.CharField(max_length=15, null=False)
       password = pw.CharField(max_length=124, null=False)
       isadmin = pw.BooleanField(default=False)
 
       class Meta:
              db_table = "users"
              order_by = ('id',)
       
