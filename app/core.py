import os
#import logging
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.exceptions import NotFound
from config.database import db
from app.utils import logapp, register_bp
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
       
       @app.before_request
       def before_request():
              #if ('user_id' not in session and 
              #(request.blueprint is None or request.blueprint != 'auth') and
              #request.endpoint != 'static'):
                     #return redirect(url_for('auth.login', next=request.url))
              bp = request.blueprint or request.endpoint
              if bp in ('auth', 'static'):
                     return
              elif 'user_id' not in session:
                     return redirect(url_for('auth.login', 
                                             next=request.url or 'static'))
              
       if not app.debug:              @app.errorhandler(Exception)
              def handle_error(e):
                     if type(e)==NotFound:
                            code = 404
                     else:
                            code = 500
                     return render_template(str(code)+'.html'), code
       
       return app

                            
       
                            
              
       
