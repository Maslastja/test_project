from app.core import create_app
from app.commands import dbase

app = create_app()
app.cli.add_command(dbase)

#app.run('localhost', 8080)
