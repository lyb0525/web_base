#! encoding=utf-8

from flask.ext.script import (Server, Shell, Manager)
from app import create_app
from app.foundation import db

app = create_app()
# app.debug = True
manager = Manager(app)

manager.add_command("runserver", Server('0.0.0.0', port=22210))
manager.add_command("shell", Shell(make_context=dict()))


@manager.command
def createtables():
    "Creates database tables"
    db.create_all()


if __name__ == "__main__":
    manager.run()
