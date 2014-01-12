#!/usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess

import requests

from flask.ext.script import Manager, Shell, Server
# from flask.ext.migrate import MigrateCommand

from budgetApp.app import create_app
# from budgetApp.user.models import User
from budgetApp.settings import DevConfig, ProdConfig
from budgetApp.extensions import db

if os.environ.get("BUDGETAPP_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)
TEST_CMD = "pytest"


def _make_context():
    """
    Return context dict for a shell session so you can access app, db, and the
    User model by default.
    """
    return {
        "app": app,
        "db": db,
        "requests": requests,
        "HOST": "http://127.0.0.0:5000/",
        # "User": User
    }


@manager.command
def test():
    """Run the tests."""
    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context))
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
