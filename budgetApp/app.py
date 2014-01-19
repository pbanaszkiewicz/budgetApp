# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.restful import Api

from .settings import ProdConfig
# from .assets import assets
from .extensions import db
# from budgetApp import public, user


def create_app(name_handler, config_object=ProdConfig, set_up_extensions=True):
    """
    Application factory (http://flask.pocoo.org/docs/patterns/appfactories/)

    :param name_handler: name the application is created and bounded to.
    :param config_object: The configuration object to use.
    :param bool set_up_extensions: register all used extensions.
    """
    app = Flask(name_handler)
    app.config.from_object(config_object)
    register_api(app)
    if set_up_extensions:
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
    api.add_resource(UserResource, "/users/<int:user_id>")

    # users' budgets
    from .views.budgets import UsersBudgetList
    api.add_resource(UsersBudgetList, "/users/<int:user_id>/budget")

    # budgets
    from .views.budgets import BudgetResource
    api.add_resource(BudgetResource, "/budget/<int:budget_id>")

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
