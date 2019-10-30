from app.core import create_app

app = create_app()
if app.debug:
    from app.commands import dbase
    app.cli.add_command(dbase)

#app.run('localhost', 8080)
