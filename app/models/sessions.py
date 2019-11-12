import peewee as pw
from flask import session
from datetime import datetime
from config.database import db
from app.models.users import User

class Sessions(db.Model):
       id = pw.PrimaryKeyField(null=False)
       token = pw.CharField(null=False)
       user = pw.ForeignKeyField(User, null=False)
       DateCreate = pw.DateTimeField()
       DateLastReq = pw.DateTimeField()
       
       class Meta:
              db_table = "sessions"
              order_by = ('id',)
       
       def save_session(user):
              if session.user:
                     row = Sessions(
                            token = session.sid,
                            user = session.user['user_id'],
                            DateCreate = datetime.today(),
                            DateLastReq = datetime.today()
                            )
                     row.save()

       def delete_session():
              result = (Sessions.delete()
                     .where(Sessions.token == session.sid)
                     .execute())
       
       def change_last_req():
              s = (Sessions.select()
                   .where(Sessions.token == session.sid)).get()
              s.DateLastReq = datetime.today()
              s.save()
       
       def exist_session():
              sid = session.sid
              s = Sessions.get_or_none(Sessions.token == sid)
              return s
       
