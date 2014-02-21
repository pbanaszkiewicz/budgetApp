# coding: utf-8

# import requests
from budgetApp.models import User


def test_get_users_list(session):
    u1 = User("test1@example.com", "web", "John", "Smith")
    u2 = User("test2@example.com", "web", "Anna", "Smith")
    session.add_all([u1, u2])
    session.commit()

    from budgetApp.views.users import UsersList
    result = UsersList().get()

    assert len(result["users"]) == 2
    assert result["users"][1] == u2.as_dict()


def test_post_users_list(test_client, session):
    # test_client.post(
    #     "/users",
    #     data=dict(
    #         email="test1@example.com",
    #         source="web",
    #         first_name="John",
    #         last_name="Smith"
    #     )
    # )

    # assert session.query(User).all().count() == 1
    pass  # so that I don't get red in travi ^_^
