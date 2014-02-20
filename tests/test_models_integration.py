# coding: utf-8
import pytest
from delorean import Delorean
from sqlalchemy.sql import func
from budgetApp.models import User, Budget
# from .test_budget_model import test_user


def sample_data():
    u1 = User("test1@example.com", "web", "John", "Smith")
    u2 = User("test2@example.com", "web", "Anna", "Smith")
    b11 = Budget("Soap", "toiletry", Delorean().datetime, 5.55, u1)
    b12 = Budget("Bread", "food", Delorean().datetime, 2.00, u1)
    b21 = Budget("Fine restaurant", "restaurants", Delorean().datetime, 90.98,
                 u2)
    return u1, u2, b11, b12, b21


@pytest.mark.slowtest
def test_user_budget_integration(session):
    u1, u2, b11, b12, b21 = sample_data()

    session.add_all([u1, u2])
    session.add_all([b11, b12, b21])
    session.commit()

    # test session integration
    assert u1.budgets == [b11, b12]
    assert u2.budgets == [b21, ]
    assert b11.user == u1
    assert b12.user == u1
    assert b21.user == u2

    # test database integration
    assert session.query(User).all() == [u1, u2]
    assert session.query(Budget).filter(Budget.user == u1).all() == [b11, b12]
    assert session.query(Budget).filter(Budget.user == u2).all() == [b21, ]
    assert session.query(func.sum(Budget.value)).scalar() == 5.55 + 2 + 90.98
    assert (session.query(func.sum(Budget.value))
                   .join(User.budgets)
                   .group_by(User.email)
                   .all()) == [(7.55,), (90.98,)]


@pytest.mark.slowtest
def test_user_budget_removal1(session):
    u1, u2, b11, b12, b21 = sample_data()

    session.add_all([u1, u2])
    session.add_all([b11, b12, b21])
    session.commit()

    assert session.query(User).all() == [u1, u2]
    assert session.query(Budget).all() == [b11, b12, b21]

    session.delete(u1)
    session.commit()
    assert session.query(User).all() == [u2, ]
    assert session.query(Budget).all() == [b21, ]

    session.delete(b21)
    session.commit()
    assert session.query(User).all() == [u2, ]
    assert session.query(Budget).all() == []


@pytest.mark.slowtest
def test_user_budget_removal2(session):
    u1, u2, b11, b12, b21 = sample_data()

    session.add_all([u1, u2])
    session.add_all([b11, b12, b21])
    session.commit()

    assert session.query(User).all() == [u1, u2]
    assert session.query(Budget).all() == [b11, b12, b21]

    # check ON DELETE CASCADE
    session.query(User).filter(User.id == u1.id).delete()
    assert session.query(User).all() == [u2, ]
    assert session.query(Budget).all() == [b21, ]

    session.query(Budget).filter(Budget.id == b21.id).delete()
    assert session.query(User).all() == [u2, ]
    assert session.query(Budget).all() == []
