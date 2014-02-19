# coding: utf-8
import pytest
from sqlalchemy.exc import IntegrityError
from budgetApp.models import User


@pytest.mark.slowtest
def test_user_created(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    session.add(u1)
    session.commit()
    assert u1.id is not 0


@pytest.mark.slowtest
def test_user_unique(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    u2 = User("test@example.com", "web", "Anna", "Smith")
    session.add(u1)
    session.commit()  # fails due to transactions not working :C
    with pytest.raises(IntegrityError):
        session.add(u2)
        session.commit()
    assert u1.id is not 0
    assert u2.id is None


@pytest.mark.slowtest
def test_user_dbrelation(session):
    # print(session.query(User).all())
    u1 = User("test@example.com", "web", "John", "Smith")
    session.add(u1)
    session.commit()  # fails due to transactions not working :C
    assert u1.budgets == []
