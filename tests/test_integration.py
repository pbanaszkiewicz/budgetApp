# coding: utf-8
import pytest
from budgetApp.models import User, Budget


def test_user_model(session):
    user1 = User("test@test", "twitter", "Adam", "Kowalski")
    session.add(user1)
    session.commit()
    assert user1.id > 0
