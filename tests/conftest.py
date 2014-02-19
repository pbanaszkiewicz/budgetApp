import pytest

from budgetApp.settings import TestConfig
from budgetApp.app import create_app
from budgetApp.models import Base


@pytest.fixture(scope="session")
def app(request):
    """
    Flask application object factory for testing session with database
    connection.
    """
    app = create_app(__name__, config_object=TestConfig, set_up_database=False)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope="session")
def app_no_db(request):
    """
    Flask application object factory for testing session.  Doesn't initialize
    database connection!
    """
    app = create_app(__name__, config_object=TestConfig, set_up_database=False)
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
    from budgetApp.app import DbSession as _db
    _db.app = app
    _db.app.connection = _db.app.engine.connect()
    Base.metadata.create_all(bind=app.engine)
    # apply migrations here

    def teardown():
        Base.metadata.drop_all(bind=app.engine)
        _db.app.connection.close()
    request.addfinalizer(teardown)

    return _db


@pytest.fixture(scope="function")
def session(db, request):
    """
    Creates a new database session (with working transaction) for a test
    duration.
    """
    db.app.transaction = db.app.connection.begin_nested()

    session = db()

    def teardown():
        session.close()
        db.app.transaction.rollback()  # Y U NO WORKIN !!!
        # print(session, dir(session))

    request.addfinalizer(teardown)
    return session
