import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from budgetApp.settings import TestConfig
from budgetApp.app import create_app
from budgetApp.models import Base


@pytest.fixture(scope="session")
def app(request):
    """
    Flask application object factory for testing session with database
    connection.
    """
    app = create_app(__name__, config_object=TestConfig, set_up_database=True)
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
def db(app_no_db, request):
    """
    Database object for testing session.
    """
    # from budgetApp.app import DbSession as _db
    # _db.app = app
    # _db.app.connection = _db.app.engine.connect()
    # Base.metadata.create_all(bind=app.engine)
    # apply migrations here

    # TODO: add database connecting here
    _app = app_no_db

    _app.engine = create_engine(_app.config["SQLALCHEMY_DATABASE_URI"])
    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()

    _app.sessionmaker = sessionmaker()

    def teardown():
        # Base.metadata.drop_all(bind=app.engine)
        # _db.app.connection.close()
        _app.connection.close()
        Base.metadata.drop_all(bind=_app.engine)
    request.addfinalizer(teardown)

    return _app


@pytest.fixture(scope="function")
def session(db, request):
    """
    Creates a new database session (with working transaction) for a test
    duration.
    """
    db.transaction = db.connection.begin()
    session = db.sessionmaker(bind=db.connection)

    def teardown():
        session.close()
        db.transaction.rollback()
    request.addfinalizer(teardown)

    return session
