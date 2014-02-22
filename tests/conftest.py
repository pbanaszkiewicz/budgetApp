import pytest

from sqlalchemy import event
from sqlalchemy.engine import Engine

import budgetApp
from budgetApp.settings import TestConfig
from budgetApp.app import create_app
from budgetApp.models import Base


@pytest.yield_fixture(scope="session")
def app():
    """
    Creates a new Flask application for a test duration.  Uses application
    factory from `budgetApp.app.create_app`.  For a tests using SQLite DB,
    a `PRAGMA foreign_keys=ON` is issued (it helps with ON DELETE CASCADE).
    """
    _app = create_app("testingsession", config_object=TestConfig)

    if _app.config["SQLALCHEMY_DATABASE_URI"].lower().startswith("sqlite"):
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """
            Make SQLite recognize ON DELETE CASCADE.
            """
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()

    # No idea why, but between this app() fixture and session() fixture there
    # is being created a new session object somewhere.  And in my tests I found
    # out that in order to have transactions working properly, I need to have
    # all these scoped sessions configured to use current connection.
    budgetApp.app.DbSession.configure(bind=_app.connection)

    yield _app

    # the code after yield statement works as a teardown
    _app.connection.close()
    Base.metadata.drop_all(bind=_app.engine)


@pytest.yield_fixture(scope="function")
def session(app):
    """
    Creates a new database session (with working transaction) for a test
    duration.
    """
    app.transaction = app.connection.begin()
    app.testing = True

    # pushing new Flask application context for multiple-thread tests to work
    ctx = app.app_context()
    ctx.push()

    session = budgetApp.app.DbSession()

    yield session

    # the code after yield statement works as a teardown
    app.transaction.close()
    session.close()
    ctx.pop()


@pytest.yield_fixture(scope="function")
def test_client(app):
    yield app.test_client()
