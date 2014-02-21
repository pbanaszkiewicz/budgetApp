import pytest

from sqlalchemy import event
from sqlalchemy.engine import Engine

import budgetApp
from budgetApp.settings import TestConfig
from budgetApp.app import create_app
from budgetApp.models import Base


@pytest.fixture(scope="session")
def app(request):
    _app = create_app("testingsession", config_object=TestConfig)

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

    def teardown_request():
        _app.connection.close()
        Base.metadata.drop_all(bind=_app.engine)
    request.addfinalizer(teardown_request)

    return _app


@pytest.fixture(scope="function")
def session(app, request):
    """
    Creates a new database session (with working transaction) for a test
    duration.
    """
    app.transaction = app.connection.begin()
    app.testing = True
    # ctx = app.app_context()
    # ctx.push()
    session = budgetApp.app.DbSession()

    def teardown():
        app.transaction.close()
        session.close()
        # ctx.pop()
    request.addfinalizer(teardown)

    return session


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()
