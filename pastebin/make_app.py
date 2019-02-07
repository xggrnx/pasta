from flask import Flask
from flask_admin.menu import MenuLink
from flask_security import SQLAlchemyUserDatastore

from pastebin.controllers.admin import AdminView, PastebinAdminIndexView
from pastebin.controllers.errors import ErrorsBlueprint
from pastebin.controllers.users import UserBlueprint
from pastebin.forms.extforms import ExtendedRegisterForm

from pastebin.controllers.index import IndexBlueprint
from pastebin.api.index import ApiBlueprint

from pastebin.models import db, security, migrate, admin
from pastebin.models.models import Role, User, Codelanguages
from pastebin.security import user_datastore
from pastebin.settings import ProdConfig
from pastebin.utils.code_langs import get_code_langs


def make_app(config_object=ProdConfig):
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='')
    app.config.from_object(config_object)
    register_extentions(app)
    register_blueprints(app)
    register_admin(app)
    register_decorators(app)

    return app


def register_blueprints(app):
    app.register_blueprint(IndexBlueprint)
    app.register_blueprint(ErrorsBlueprint)
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(ApiBlueprint)


def register_extentions(app):
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)
    migrate.init_app(app, db)


def register_admin(app):
    admin.init_app(app, index_view=PastebinAdminIndexView())
    admin.add_view(AdminView(User, db.session))
    admin.add_link(MenuLink(name='Back Home', url='/'))


def register_decorators(app):
    @app.before_first_request
    def before_first_request():
        db.create_all()
        admin_role = 'admin'
        admin_email = 'admin@green.ru'

        if not user_datastore.get_user(admin_email):
            user_datastore.create_user(
                email=admin_email, name=admin_role,
                password='123pass',
                api_key='123123123'
            )

        db.session.commit()
        for code in get_code_langs():
            exist = db.session.query(Codelanguages).filter_by(id=code[0]).first()
            if not exist:
                db.session.add(Codelanguages(id=code[0], name=code[1], is_active=code[2]))

        db.session.commit()

        exist = db.session.query(Role).filter_by(name='user').first()
        if not exist:
            db.session.add(Role(name='user', description="default user"))

        db.session.commit()

        user_datastore.add_role_to_user(admin_email, admin_role)

        db.session.commit()
