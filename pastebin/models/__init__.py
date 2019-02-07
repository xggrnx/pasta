from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_admin import Admin
from flask_migrate import Migrate
from celery import Celery

db = SQLAlchemy()
security = Security()
migrate = Migrate()
celery = Celery()
admin = Admin(name='502paste', template_mode='bootstrap3')