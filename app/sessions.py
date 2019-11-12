import secrets
from flask import request
from flask.sessions import SessionInterface, SessionMixin
from app.models.sessions import Sessions
from werkzeug.datastructures import CallbackDict

class MyDatabaseSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False
        self.accessed = False
        self.user = None
        self.sid = None
        
class MyDatabaseSessionInterface(SessionInterface):
    session_class = MyDatabaseSession
    
    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        s = self.session_class()
        if not sid:
            sid = secrets.token_hex(24)
            s.sid = sid
        
        sbd = Sessions.get_or_none(Sessions.token == sid)
        s.sid = sid
        if sbd:
            user = {
                    'user_id': sbd.user.id,
                    'username': sbd.user.username,
                    'isadmin': sbd.user.isadmin,
                }
            s.user = user
        return s
            
    def save_session(self, app, session, response):
        s = Sessions.exist_session()
        if not s:
            if session.modified:
                response.delete_cookie(app.session_cookie_name)
                return
        
        sid = request.cookies.get(app.session_cookie_name)
        #if sid is None: #тоже вариант
        if session.user and sid != session.sid:
            response.set_cookie(app.session_cookie_name, session.sid)
 