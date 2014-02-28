# coding: utf-8
import pytest
from sqlalchemy.exc import IntegrityError
from budgetApp.models import User


@pytest.mark.fasttest
def test_user_created(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    session.add(u1)
    session.commit()
    assert u1.id is not 0
    assert session.query(User).count() == 1


@pytest.mark.fasttest
def test_user_unique(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    u2 = User("test@example.com", "web", "Anna", "Smith")
    session.add(u1)
    session.commit()
    assert u1.id is not 0

    # this with-statement block rolls back transaction, so I include assert
    # for an object successfully created *within* transaction before the
    # rollback
    with pytest.raises(IntegrityError):
        session.add(u2)
        session.commit()

    assert u2.id is None


@pytest.mark.fasttest
def test_user_dbrelation(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    session.add(u1)
    session.commit()
    assert u1.budgets == []
