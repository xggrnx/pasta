import requests

from flask import Blueprint
from flask_login import login_required


PostOfficeBlueprint = Blueprint('PostOffice', __name__, url_prefix='/post/')


class PostOffice():
    @staticmethod
    @PostOfficeBlueprint.route('/', methods=['GET'])
    @login_required
    def index():
        pass

