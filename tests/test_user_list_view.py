# coding: utf-8

from budgetApp.models import User


def test_get_users_list(session):
    """Test for GET /users"""
    from budgetApp.views.users import UsersList
    result, code = UsersList().get()
    assert code == 200  # even though we have no users

    """Test for GET /users"""
    u1 = User("test1@example.com", "web", "John", "Smith")
    u2 = User("test2@example.com", "web", "Anna", "Smith")
    session.add_all([u1, u2])
    session.commit()

    result, code = UsersList().get()

    assert len(result["users"]) == 2
    assert result["users"][1] == u2.as_dict()
    assert code == 200


def test_post_users_list(app, session):
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
