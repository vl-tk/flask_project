"""Authentication middleware in third party app Kratos."""
import requests
from flask import Request, redirect


class SimpleMiddleWare(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print('something you want done in every http request')
        return self.app(environ, start_response)
