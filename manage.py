#!/usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess

import requests

from flask.ext.script import Manager, Shell, Server
# from flask.ext.migrate import MigrateCommand

from budgetApp.app import DbSession, create_app
from budgetApp.models import Base, User, Budget
from budgetApp.settings import DevConfig, ProdConfig
# from budgetApp.extensions import db

if os.environ.get("BUDGETAPP_ENV") == 'prod':
    app = create_app(__name__, ProdConfig)
else:
    app = create_app(__name__, DevConfig)

manager = Manager(app)


def _make_context():
    """
    Return context dict for a shell session so you can access app, db, and the
    User model by default.
    """
    from budgetApp.serializers import UserSerializer, BudgetSerializer
    return {
        "app": app,
        "db": DbSession(),
        "requests": requests,
        "HOST": "http://127.0.0.1:5000",
        "User": User,
        "Budget": Budget,
        "UserSerializer": UserSerializer,
        "BudgetSerializer": BudgetSerializer,
    }


@manager.command
def test():
    """Run the tests."""
    status = subprocess.call("pytest", shell=True)
    sys.exit(status)


@manager.command
def createdb():
    """Create tables in database."""
    Base.metadata.create_all(bind=app.engine)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context,
                                   use_ipython=True))
# manager.add_command('migratedb', MigrateCommand)

if __name__ == '__main__':
    manager.run()
