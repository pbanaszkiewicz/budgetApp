# coding: utf-8

from flask import json
from budgetApp.models import User


def test_get_users_list(session):
    """Test for GET /users"""
    u1 = User("test1@example.com", "web", "John", "Smith")
    u2 = User("test2@example.com", "web", "Anna", "Smith")
    session.add_all([u1, u2])
    session.commit()

    from budgetApp.views.users import UsersList
    result, code = UsersList().get()

    assert len(result["users"]) == 2
    assert result["users"][1] == u2.as_dict()
    assert code == 200


def test_post_users_list(test_client, session):
    """Test for POST /users"""
    result = test_client.post(
        "/users",
        data=dict(
            email="test1@example.com",
            source="web",
            first_name="John",
            last_name="Smith"
        )
    )
    contents = json.loads(result.data)

    assert session.query(User).count() == 1
    assert result.status_code == 201
    assert (contents["user"] == session.query(User)
                                       .get(contents["user"]["id"]).as_dict())


def test_post_users_list2(app, session):
    """Test for POST /users"""
    data = dict(
        email="test1@example.com",
        source="web",
        first_name="John",
        last_name="Smith"
    )
    with app.test_request_context("/users", method="POST", data=data):
        from budgetApp.views.users import UsersList
        result, code = UsersList().post()

        assert session.query(User).count() == 1
        assert code == 201
        assert (result["user"] == session.query(User)
                                         .get(result["user"]["id"]).as_dict())