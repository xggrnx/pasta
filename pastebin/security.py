from flask_security import SQLAlchemyUserDatastore

from pastebin.models import db
from pastebin.models.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)