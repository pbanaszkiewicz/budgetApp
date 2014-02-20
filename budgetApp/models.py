# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    source = Column(String(30))
    first_name = Column(String(30))
    last_name = Column(String(30))

    # I prefer explicit 2-way relationship than implicit
    budgets = relationship("Budget", back_populates="user",
                           cascade="all,delete")

    def __init__(self, email, source, first_name, last_name):
        self.email = email
        self.source = source
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return u'<{} {} ({})>'.format(self.first_name, self.last_name,
                                      self.email)


class Budget(Base):
    """Budget item model for specific User."""
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    description = Column(String(80))
    date = Column(DateTime)
    value = Column(Float)

    # I prefer explicit 2-way relationship than implicit
    user = relationship("User", back_populates="budgets")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __init__(self, description, category, date, value, user):
        self.description = description
        self.category = category
        self.date = date
        self.value = value
        # self.user_id = user.id
        self.user = user

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return u'<{} ({}): {} on {}>'.format(self.description, self.category,
                                             self.value, self.date)
