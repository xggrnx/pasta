import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config():
    DOMAIN = 'localhost'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "APPSEKRETKEYxzcz13421"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "APPSALT"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "token"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_LOGIN_URL = "/login"
    SECURITY_REGISTER_URL = "/register"
    SECURITY_LOGOUT_URL = "/logout"
    WTF_CSRF_ENABLED = False
    SECURITY_CHANGEABLE = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    UPLOAD_FOLDER = os.path.join(APP_DIR, 'static', 'uploads')


class CeleryConf():
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


class DevConfig(Config, CeleryConf):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PASTA_DATABASE_URL',
                                             'postgresql://pasteuser:14881488@localhost/pastebin')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config, CeleryConf):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PASTA_DATABASE_URL',
                                             'postgresql://pasteuser:14881488@localhost/pastebin')