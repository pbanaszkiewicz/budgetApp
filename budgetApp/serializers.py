# coding: utf-8
from marshmallow import Serializer, fields


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email", "source", "first_name", "last_name")


class BudgetSerializer(Serializer):
    user = fields.Nested(UserSerializer)

    class Meta:
        fields = ("id", "user", "category", "description", "date", "value")
