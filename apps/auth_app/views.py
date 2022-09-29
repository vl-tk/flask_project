from . import auth
from database import db


from flask import render_template, request, redirect, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from .forms import LoginForm, RegistrationForm


@auth.route("/user/<int:user_id>")
@login_required
def user_profile(user_id):
    return render_template("base.html", title="MicroApp")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    form = LoginForm(request.form)
    # print(form.data)
    # print(form.errors)
    if form.validate_on_submit():
        login_user(form.get_user(), remember=True)
        return redirect("/")
    return render_template("auth_app/login.html", title="MicroApp", form=form)


@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():

    from models import User

    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        login_user(user, remember=True)
        return redirect("/")
    return render_template("auth_app/register.html", title="MicroApp", form=form)
