# coding: utf-8

import pytest
from budgetApp.models import User


@pytest.fixture(scope="function")
def user1():
    return User("test1@example.com", "web", "John", "Smith")


@pytest.fixture(scope="function")
def user2():
    return User("test2@example.com", "web", "Anna", "Smith")


def test_get_user(user1, user2, session):
    """
    Test for GET /users/:user_id: -- test successfully getting a specific
    user.
    """
    session.add(user1)
    session.add(user2)
    session.commit()

    from budgetApp.views.users import UserResource
    result, code = UserResource().get(user1.id)

    assert code == 200
    assert result["user"] == user1.as_dict()


def test_put_user(user1, user2, app, session):
    """Test for PUT /users/:user_id: -- test updating specific user."""
    session.add(user1)
    session.add(user2)
    session.commit()

    data = dict(
        email="test3@example.org",
        source="fanpage",
        first_name=user1.first_name,
        last_name=user1.last_name,
    )

    with app.test_request_context("/users/{}".format(user1.id), method="PUT",
                                  data=data):
        from budgetApp.views.users import UserResource
        result, code = UserResource().put(user1.id)

        assert session.query(User).count() == 2
        assert code == 201

        # SQLAlchemy updated user1 automatically behind the scenes
        assert result["user"] == user1.as_dict()


def test_delete_user(user1, user2, session):
    """Test for DELETE /users/:user_id: -- test removing specific user."""
    session.add(user1)
    session.add(user2)
    session.commit()
    assert session.query(User).count() == 2

    from budgetApp.views.users import UserResource
    result, code = UserResource().delete(user1.id)

    assert code == 204
    assert session.query(User).count() == 1
    # assert user1 is None
