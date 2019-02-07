from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_security import login_required, current_user
from pastebin.forms.profile import EditProfileForm
from pastebin.models.models import Pastes, User
from pastebin.models import db
import uuid, datetime
from pastebin.forms.pastes import PastesForm, PastesFormGet, getLifeTime

IndexBlueprint = Blueprint('Index', __name__, url_prefix='')


def last_pasts():
    """
    :return: List of resent posts
    """
    timenow = datetime.datetime.now()
    query = db.session.query(Pastes).filter(Pastes.private == False, Pastes.date_timelive > timenow).order_by(
        Pastes.id.desc()).limit(10)
    return query


class IndexView(object):
    @staticmethod
    @IndexBlueprint.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
        form = PastesForm()
        if form.validate_on_submit():
            request_paste = Pastes()
            if form.title.data:
                request_paste.title = form.title.data
            else:
                request_paste.title = "Untitled"

            request_paste.link = uuid.uuid4().hex
            request_paste.paste = form.paste.data
            request_paste.date = datetime.datetime.now()
            request_paste.date_timelive = getLifeTime(curr=request.form.get('date_timelive'))
            request_paste.private = form.is_private.data
            request_paste.user_id = current_user.id
            request_paste.code_id = request.form.get('code_id')
            db.session.add(request_paste)
            try:
                db.session.flush()
                db.session.commit()
            except:
                db.session.rollback()

            return redirect(url_for('Index.pastes', link=request_paste.link))

        return render_template('index.html', form=form, last_pasts=last_pasts())


class PostView(object):
    @staticmethod
    @IndexBlueprint.route('/pastes/<link>', methods=['GET', 'POST'])  # @такая же ебала как и в юзерах
    def pastes(link):
        timenow = datetime.datetime.now()
        try:
            paste = db.session.query(Pastes).filter(Pastes.link == link, Pastes.date_timelive > timenow).one()
            return render_template('pastes.html', paste=paste, last_pasts=last_pasts())

        except:
            return render_template('404.html'), 404


class MyPastesView(object):
    @staticmethod
    @IndexBlueprint.route('/mypastes/', methods=['GET', 'POST'])
    @login_required
    def my_pastes():
        form = PastesFormGet()
        query_args = []
        timenow = datetime.datetime.now()
        query_args.append("user_id = {0}".format(current_user.id))
        query_args.append("date_timelive > '{0}'".format(timenow))

        if request.args.get('code_id') and request.args.get('code_id') != '1':  # 1 - Selected Syntax: None
            query_args.append("code_id = {0}".format(request.args.get('code_id')))

        if request.args.get('title'):
            query_args.append("title = '{0}'".format(request.args.get('title')))

        if request.args.get('is_private'):
            query_args.append(
                "private = True")  # Является ли паста приватной

        try:
            query = db.session.query(Pastes) \
                .filter(*query_args) \
                .order_by(Pastes.id.desc()).limit(10)
            return render_template('mypastes.html', last_pasts=last_pasts(), my_pasts=query, form=form)
        except:
            query = db.session.query(Pastes) \
                .filter(Pastes.user_id == current_user.id) \
                .order_by(Pastes.id.desc()).limit(10)
            return render_template('mypastes.html', last_pasts=last_pasts(), my_pasts=query, form=form)
