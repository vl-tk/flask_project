import flask_admin as admin
import flask_login as login
from flask.views import MethodView
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    """
    TODO: move to admin
    """

    def is_accessible(self):
        return login.current_user.is_authenticated


class CustomUserView(MyModelView):
    pass


class AnotherAdminView(admin.BaseView):
    # TODO: test

    @admin.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @admin.expose('/test/')
    # {{ url_for('.test') }}
    def test(self):
        return self.render('test.html')


class ViewWithMethodViews(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('methodtest.html')

    @admin.expose_plugview('/_api/1')
    class API_v1(MethodView):
        def get(self, cls):
            return cls.render('test.html', request=request, name="API_v1")

        def post(self, cls):
            return cls.render('test.html', request=request, name="API_v1")

    @admin.expose_plugview('/_api/2')
    class API_v2(MethodView):
        def get(self, cls):
            return cls.render('test.html', request=request, name="API_v2")

        def post(self, cls):
            return cls.render('test.html', request=request, name="API_v2")
