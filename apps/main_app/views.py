# -*- coding: utf-8 -*-
from flask import jsonify
from flask import render_template

from . import main


@main.route("/")
def index_page():
    return render_template("base.html", title="Project title")


@main.route("/ping")
def ping():
    return {"test": "Button1"}


"""
from flask_wtf.csrf import CSRFProtect, generate_csrf
@main.route("/csrf-cookie/", methods=["GET"])
def token():
    res = {"csrfToken": generate_csrf()}
    return jsonify(res)
"""
