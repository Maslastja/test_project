import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db

class User(db.Model):
       id = pw.PrimaryKeyField(null=False)
       username = pw.CharField(max_length=15, null=False)
       password = pw.CharField(max_length=124)
       isadmin = pw.BooleanField(default=False)
 
       class Meta:
              db_table = "users"
              order_by = ('id',)

       def set_password(self, password):
              self.password = generate_password_hash(password)
          
       def check_password(self, password):
              return check_password_hash(self.password, password)
       
       