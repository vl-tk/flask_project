import os


class BaseConfig:
    """
    see .flaskenv for env values
    """

    LANGUAGES = ['ru', 'en']

    # so we can use sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')

    # if sqlite will be used, uncomment
    # DB_PATH = os.environ.get('DB_PATH', 'db/base.db')
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 5432)
    DB_NAME = os.environ.get('DB_NAME', 'demo')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', '123456')

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        DB_USER,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )

    # REST API CONFIG
    """
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_ERROR_404_HELP = True
    """


class DevConfig(BaseConfig):
    """Development configuration options"""

    pass


class TestConfig(BaseConfig):
    """Testing configuration options"""

    ENV = 'testing'

    TESTING = True
    WTF_CSRF_ENABLED = False
    # or use https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
    # to test with csrf protection as well

    LANGUAGES = ['ru', 'en']

    # so we can use sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')

    # uncomment if sqlite is used
    # DB_PATH = os.environ.get('DB_PATH', 'db/base.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 5432)
    DB_NAME = os.environ.get('DB_NAME', 'demo')  # or create test_db for testing purpose
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', '123456')

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        DB_USER,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME
    )
