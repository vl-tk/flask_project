#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from secure import SecureHeaders

from flask_migrate import Migrate

from flask_cors import CORS

from flask_login import LoginManager  # user session manager

from flask_babel import Babel

from flask_debugtoolbar import DebugToolbarExtension

import flask_admin
from flask_admin.contrib.sqla import ModelView

from database import db  # isort:skip

from apps.main_app import main
# from apps.api_app import api
# from apps.students_app import students
# from apps.demo_app import demo
from apps.auth_app import auth
# from apps.forms_app import forms_demo

# import ssl
# context = ssl.SSLContext()
# context.load_cert_chain('certs/localhost.crt', 'certs/localhost.key')
# server.crt = fullchain.pem, server.key = privkey.pem - if used LetsEncrypt Certbot

import config  # isort:skip

# from middleware import AuthMiddleware

secure_headers = SecureHeaders()


def register_blueprints(app):
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    # app.register_blueprint(api, url_prefix="/api/v1")
    # app.register_blueprint(demo, url_prefix="/demo")
    # app.register_blueprint(students, url_prefix="/students")
    # app.register_blueprint(forms_demo, url_prefix="/forms")


def create_app(config=config.BaseConfig):
    """Return an initialized Flask application."""

    app = Flask(__name__, static_url_path="/static", static_folder="static")
    app.config.from_object(config)

    # the toolbar is only enabled in debug mode:
    app.debug = True

    toolbar = DebugToolbarExtension(app)

    register_blueprints(app)

    """
    register_extensions(app)
    register_errorhandlers(app)
    register_jinja_env(app)
    register_commands(app)
    """

    @app.after_request
    def set_secure_headers(response):
        # secure_headers.flask(response)
        return response

    @app.shell_context_processor
    def make_shell_context():
        """Populate shell with models.

        TODO: add models from other blueprints
        """

        import inspect
        import models

        MODELS_MODULES = [models]

        res = {"db": db}
        for module in MODELS_MODULES:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    res[name] = obj

        return res

    return app


def create_logger(name):
    """Creating logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # create file handler for logger
    fh = RotatingFileHandler(f"logs/{name}.log", maxBytes=5000000, backupCount=8)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        """
        user loader function
        Given *user_id*, return the associated User object.
        """
        from models import User

        return db.session.query(User).get(user_id)


def init_admin(app, db):

    from models import User
    from admin import CustomUserView, MyModelView

    admin_panel = flask_admin.Admin(app, name="Project", template_mode="bootstrap4")
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    admin_panel.add_view(CustomUserView(User, db.session))

    # from apps.students_app.models import Student, Exam, Course, Teacher

    # admin_panel.add_view(MyModelView(Course, db.session, category="Education"))
    # admin_panel.add_view(MyModelView(Exam, db.session, category="Education"))

    # from apps.students_app.admin import CustomStudentView, CustomTeacherView

    # admin_panel.add_view(
    #     CustomStudentView(
    #         Student, db.session, category="Education", name="student_view"
    #     )
    # )
    # admin_panel.add_view(CustomTeacherView(Teacher, db.session, category="Education"))

    # from apps.demo_app.models import (
    #     Ticket,
    #     Booking,
    #     AircraftsDatum,
    #     AirportsDatum,
    #     Flight,
    #     Seat,
    #     TicketFlight,
    #     BoardingPass,
    # )

    # admin_panel.add_view(MyModelView(Booking, db.session, category="AirDB"))
    # admin_panel.add_view(MyModelView(AircraftsDatum, db.session, category="AirDB"))
    # admin_panel.add_view(MyModelView(AirportsDatum, db.session, category="AirDB"))
    # admin_panel.add_view(MyModelView(Flight, db.session, category="AirDB"))

    # from apps.demo_app.admin import (
    #     CustomTicketView,
    #     CustomTicketFlightView,
    #     CustomBoardingPass,
    # )

    # admin_panel.add_view(CustomTicketView(Ticket, db.session, category="AirDB"))
    # admin_panel.add_view(
    #     CustomTicketFlightView(TicketFlight, db.session, category="AirDB")
    # )
    # admin_panel.add_view(CustomBoardingPass(BoardingPass, db.session, category="AirDB"))

    # from apps.forms_app.models import Race, Lap
    # from apps.forms_app.admin import CustomRaceView, CustomLapView

    # admin_panel.add_view(CustomRaceView(Race, db.session, category="FormsDemo"))
    # admin_panel.add_view(CustomLapView(Lap, db.session, category="FormsDemo"))


app = create_app()
db.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)
# csrf.exempt(api)  # we use JWT for API protection

# enable CORS
"""
It's worth noting that the above setup allows cross-origin requests on all
routes, from any domain, protocol, or port. In a production environment, you
should only allow cross-origin requests from the domain where the front-end
application is hosted. Refer to the Flask-CORS documentation for more info on
this.
"""
CORS(app, resources={r"/*": {"origins": "*"}})

migrate = Migrate(app, db)
# app.wsgi_app = AuthMiddleware(app.wsgi_app)  # for external auth via API

logger = create_logger(__name__)
init_login(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


init_admin(app, db)

if hasattr(config.BaseConfig, 'DB_PATH') and not Path(config.BaseConfig.DB_PATH).exists():
    from utils import build_sample_db

    """
    # make sure that sqlite is used, not postgres
    with app.app_context():
        build_sample_db()
    """
