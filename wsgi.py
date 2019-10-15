from app.core import create_app
from app import commands

app = create_app()
commands.register(app)

#app.run('localhost', 8080)
