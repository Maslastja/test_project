import os
import importlib
#import logging
from flask import Flask, render_template
from logging.handlers import RotatingFileHandler
from werkzeug.exceptions import NotFound
from config.database import db
from app import views
from peewee import logging

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
       #db.database.create_tables([User])
              
       @app.errorhandler(Exception)
       def handle_error(e):
              print(e)
              if type(e)==NotFound:
                     code = 404
              else:
                     code = 500
              return render_template(str(code)+'.html'), code
       
       app.add_url_rule('/login', view_func=views.login, 
                       methods=['GET', 'POST'])       
       app.add_url_rule('/index', view_func=views.index)
       app.add_url_rule('/', view_func=views.index)
       
       if not app.debug:
              if not os.path.exists('logs'):
                     os.mkdir('logs')
              file_handler = RotatingFileHandler('logs/app.log', 
                                                 maxBytes=10240, backupCount=10)
              file_handler.setFormatter(logging.Formatter(
               '%(asctime)s %(levelname)s: \
               %(message)s [in %(pathname)s:%(lineno)d]'))
              file_handler.setLevel(logging.INFO)
              app.logger.addHandler(file_handler)
       
              app.logger.setLevel(logging.INFO)
              app.logger.info('test app')
           
       return app

def register_bp(app):
       indir = 'app/'
       for address, dirs, files in os.walk(indir):
              for d in dirs:
                     path = 'app.'+d
                     module_spec = importlib.util.find_spec(path)
                     if module_spec.loader is not None:
                            module = importlib.util.module_from_spec(module_spec)
                            module_spec.loader.exec_module(module)
                            
                            #print(module.bp)
                            if 'bp' in module.__dict__:
                                   bp = module.bp
                                   if 'options' in module.__dict__:
                                          opt = module.options
                                   else:
                                          opt = {}
                                   app.register_blueprint(bp, **opt)
                            
                            
              
       
