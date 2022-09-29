# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm  # will add csrf protection
from werkzeug.security import check_password_hash
from wtforms import fields, validators
from wtforms.fields import html5

from database import db


class LoginForm(FlaskForm):
    """
    example:
    https://github.com/mrjoes/flask-admin/blob/master/examples/auth/app.py
    """

    login = fields.StringField(
        "Логин",
        validators=[validators.InputRequired(), validators.Length(min=4, max=20)],
    )
    password = fields.PasswordField(
        "Пароль",
        validators=[validators.InputRequired(), validators.Length(min=6, max=20)],
    )

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Некорректное имя пользователя")

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError("Неверный пароль")

    def get_user(self):
        from models import User

        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(FlaskForm):

    login = fields.StringField(
        "Логин",
        validators=[validators.InputRequired(), validators.Length(min=4, max=20)],
    )
    password = fields.PasswordField(
        "Пароль",
        validators=[validators.InputRequired(), validators.Length(min=6, max=20)],
    )
    email = html5.EmailField(
        "E-mail", validators=[validators.InputRequired(), validators.Email()]
    )
    first_name = fields.StringField()
    last_name = fields.StringField()

    def validate_login(self, field):
        from models import User

        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError("Логин уже занят")

    def validate_email(self, field):
        from models import User

        if db.session.query(User).filter_by(email=self.email.data).count() > 0:
            raise validators.ValidationError("E-mail уже используется")
