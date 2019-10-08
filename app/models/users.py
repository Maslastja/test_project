import peewee as pw
from config.database import db

class User(db.Model):
       id = pw.PrimaryKeyField(null=False)
       username = pw.CharField(max_length=15, null=False)
       password = pw.CharField(max_length=124, null=False)
 
       class Meta:
              db_table = "users"
              order_by = ('id',)
       
       def sel_user_by_name(username):
              return User.select().where(User.username == username)

       def get_user_by_id(id):
              return (User.select().where(User.id==id)).get()
   
