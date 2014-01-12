from .extensions import db


class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    source = db.Column(db.String(30))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    bugdets = db.relationship("Budget", backref="user", lazy="dynamic")

    def __init__(self, email, source, first_name, last_name):
        self.email = email
        self.source = source
        self.first_name = first_name
        self.last_name = last_name


class Budget(db.Model):
    """Budget item model for specific User."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.String(50))
    description = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)
