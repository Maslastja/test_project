import os
import logging
from flask import Flask, render_template
from logging.handlers import RotatingFileHandler
from config.database import db
from app.groups import bp as bp_gr
from app.students import bp as bp_st
from app.analis import bp as bp_an
from app.admin import bp as bp_adm
from app import views

def create_app():
       app = Flask('app', root_path=os.getcwd(), 
                   static_folder='static', 
                   template_folder='app/templates')
       
       app.config.from_object('config.settings')
       
       
       app.register_blueprint(bp_gr, url_prefix='/group')
       app.register_blueprint(bp_st, url_prefix='/student')
       app.register_blueprint(bp_an, url_prefix='/analis')
       app.register_blueprint(bp_adm, url_prefix='/admin')

       db.init_app(app)
       #db.database.create_tables([User])
              
       @app.errorhandler(404)
       def not_found_error(error):
              return render_template('404.html', title='404 Not found'), 404
       
       @app.errorhandler(500)
       def internal_error(error):
              return render_template('500.html', title='500 Oops!'), 500
       
       app.add_url_rule('/login', view_func=views.login, 
                       methods=['GET', 'POST'])       
       app.add_url_rule('/index', view_func=views.index)
       app.add_url_rule('/', view_func=views.index)
       
       if not app.debug:
              if not os.path.exists('logs'):
                     os.mkdir('logs')
              file_handler = RotatingFileHandler('logs/microblog.log', 
                                                 maxBytes=10240, backupCount=10)
              file_handler.setFormatter(logging.Formatter(
               '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
              file_handler.setLevel(logging.INFO)
              app.logger.addHandler(file_handler)
       
              app.logger.setLevel(logging.INFO)
              app.logger.info('Microblog startup')
           
       return app


