# coding: utf-8
from __future__ import absolute_import

from flask import Flask, render_template, _app_ctx_stack, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.restful import Api

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Query as SAQuery
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .settings import ProdConfig
# from .assets import assets
# from budgetApp import public, user

# database session registry object, configured from create_app factory
DbSession = scoped_session(sessionmaker(),
                           # __ident_func__ should be hashable, therefore used
                           # for recognizing different incoming requests
                           scopefunc=_app_ctx_stack.__ident_func__)


class BaseQuery(SAQuery):
    """
    Extended SQLAlchemy Query class, provides :meth:`BaseQuery.first_or_404`
    and :meth:`BaseQuery.get_or_404` similarily to Flask-SQLAlchemy.
    These methods are additional, :class:`BaseQuery` works like a normal
    SQLAlchemy query class.
    """

    def get_or_404(self, identity):
        result = self.get(identity)
        if result is None:
            abort(404)
        return result

    def first_or_404(self):
        result = self.first()
        if result is None:
            abort(404)
        return result


def create_app(name_handler, config_object=None):
    """
    Application factory (http://flask.pocoo.org/docs/patterns/appfactories/)

    :param name_handler: name the application is created and bounded to.
    :param config_object: the configuration object to use.
    """
    app = Flask(name_handler)
    if not config_object:
        config_object = ProdConfig
    app.config.from_object(config_object)
    app.engine = None

    app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    global DbSession
    DbSession.configure(bind=app.engine, query_cls=BaseQuery)

    @app.teardown_appcontext
    def teardown(exception=None):
        if isinstance(exception, NoResultFound) or \
           isinstance(exception, MultipleResultsFound):
            abort(404)
        global DbSession
        if DbSession:
            DbSession.remove()

    register_extensions(app)
    register_api(app)
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
    # db.init_app(app)
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
