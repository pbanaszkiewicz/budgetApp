# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.restful import Api

from budgetApp.settings import ProdConfig
# from budgetApp.assets import assets
from budgetApp.extensions import db
# from budgetApp import public, user


def create_app(config_object=ProdConfig):
    """
    Application factory (http://flask.pocoo.org/docs/patterns/appfactories/)

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_api(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_api(app):
    """
    Register Flask-RESTful APIs.
    """
    api = Api(app)

    # users
    from .views.users import UsersList, UserResource
    api.add_resource(UsersList, "/users")
    api.add_resource(UserResource, "/users/<string:user_id>")

    # users' budgets
    from .views.budgets import UsersBudgetList
    api.add_resource(UsersBudgetList, "/users/<string:user_id>/budget")

    # budgets
    from .views.budgets import BudgetResource
    api.add_resource(BudgetResource, "/budget/<string:budget_id>")

    return None


def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)
    # assets.init_app(app)
    toolbar = DebugToolbarExtension(app)
    # cache.init_app(app)
    # migrate.init_app(app, db)
    return None


def register_blueprints(app):
    # app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        return render_template("{0}.html".format(error.code)), error.code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
