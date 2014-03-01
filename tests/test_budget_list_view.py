# coding: utf-8

import pytest
from delorean import Delorean
from budgetApp.models import User, Budget


@pytest.fixture(scope="function")
def user1():
    return User("test1@example.com", "web", "John", "Smith")


@pytest.fixture(scope="function")
def sample_budgets(user1):
    b11 = Budget("Soap", "toiletry", Delorean().datetime, 5.55, user1)
    b12 = Budget("Bread", "food", Delorean().datetime, 2.00, user1)
    return [b11, b12]


@pytest.mark.xfail
def test_get_user_budgets(user1, sample_budgets, session):
    """Test for GET /users/:id:/budget"""
    session.add(user1)
    session.commit()

    from budgetApp.views.budgets import UsersBudgetList
    result, code = UsersBudgetList().get(user1.id + 1)
    assert code == 404

    result, code = UsersBudgetList().get(user1.id)
    assert code == 200
    assert result["budgets"] == [o.as_dict() for o in sample_budgets]
