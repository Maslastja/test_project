import os
#import logging
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import NotFound
from config.database import db
from app.utils import logapp, register_bp
from app.sessions import MyDatabaseSessionInterface
from app.models.sessions import SessionsStore
#logger = logging.getLogger('peewee')
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.DEBUG)

def create_app():
       app = Flask('app', root_path=os.getcwd(), 
                   static_folder='static', 
                   template_folder='app/templates')
       
       app.config.from_object('config.settings')
       register_bp(app)
       db.init_app(app)
       if not app.debug:
              logapp(app)
       
       app.session_interface = MyDatabaseSessionInterface()
       
       @app.before_request
       def before_request():
              bp = request.blueprint or request.endpoint
              if bp in ('auth', 'static'):
                     return
              if not session.user:
                     return redirect(url_for('auth.login', 
                                             next=request.url or 'static'))

       
       @app.after_request
       def after_request(response):
              s = session.exist_session()
              if s:
                     session.change_last_req()
              return response
       
              
       if not app.debug:
              @app.errorhandler(Exception)
              def handle_error(e):
                     if type(e)==NotFound:
                            code = 404
                     else:
                            code = 500
                     return render_template(str(code)+'.html'), code
       
       return app

                            
       
                            
              
       
