# -*- coding: utf-8 -*-
import datetime

from flask_login.mixins import UserMixin

from database import db


class User(UserMixin, db.Model):
    """
    Required by Flask-Login

    for Flask-Login integration UserMixin is used

    db.create_all() is required
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(256))

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.is_active_user

    def get_id(self):
        return self.id

    def __repr__(self):
        return (
            f"#{self.id} {self.login} [{self.email}] {self.first_name} {self.last_name}"
        )
