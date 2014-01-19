import pytest

from budgetApp.settings import TestConfig
from budgetApp.app import create_app
from budgetApp.extensions import db as _db


@pytest.fixture(scope="session")
def app(request):
    """
    Flask application object factory for testing session.
    """
    app = create_app(__name__, TestConfig, True)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope="session")
def db(app, request):
    """
    Database object for testing session.
    """
    def teardown():
        _db.drop_all()

    _db.app = app
    # apply migrations here
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """
    Creates a new database connection for a test duration.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
