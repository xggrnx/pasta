from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_admin import helpers, expose
from flask_admin import AdminIndexView
from flask_security import roles_accepted


class AdminView(ModelView):
    @login_required
    @roles_accepted('admin')
    def _handle_view(self, name, **kwargs):
        pass


class PastebinAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    @roles_accepted('admin')
    def index(self):
        return super(PastebinAdminIndexView, self).index()
