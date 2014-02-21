# coding: utf-8
import pytest
from delorean import Delorean
from budgetApp.models import User, Budget


@pytest.fixture(scope="function")
def test_user(session):
    u = User("test@example.com", "web", "John", "Smith")
    session.add(u)
    session.commit()
    return u


@pytest.mark.fasttest
def test_budget_created(test_user, session):
    b1 = Budget("Soap", "toiletry", Delorean().datetime, 5.55, test_user)
    session.add(b1)
    session.commit()
    assert session.query(User).count() == 1
    assert session.query(Budget).count() == 1
    assert test_user.budgets == [b1, ]
    assert b1.user_id == test_user.id


@pytest.mark.fasttest
def test_user_dbrelation(session):
    u1 = User("test@example.com", "web", "John", "Smith")
    session.add(u1)
    session.commit()
    assert u1.budgets == []
