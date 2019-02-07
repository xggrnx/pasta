from flask import Blueprint, render_template

ErrorsBlueprint = Blueprint('Errors', __name__, url_prefix='')


class Page_not_found(object):
    @staticmethod
    @ErrorsBlueprint.app_errorhandler(404)
    def handle_404(e):
        return render_template('404.html'), 404


class Server_error(object):
    @staticmethod
    @ErrorsBlueprint.app_errorhandler(500)
    def handle_500(e):
        return render_template('500.html'), 500


class Permission_error(object):
    @staticmethod
    @ErrorsBlueprint.app_errorhandler(403)
    def handle_403(e):
        return render_template('403.html'), 403
