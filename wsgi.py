from os import getenv
from app.core import create_app

app = create_app()
if getenv('DEBUG')=='True':
    from app.commands import dbase
    #print(os.getenv('DEBUG'))
    app.cli.add_command(dbase)

#app.run('localhost', 8080)
