import datetime
import os
import uuid
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from pastebin.controllers.index import last_pasts
from pastebin.forms.profile import EditProfileForm
from pastebin.models import db
from pastebin.models.models import User, Pastes
from pastebin.settings import Config

UserBlueprint = Blueprint('User', __name__, url_prefix='')


class UserView:
    @staticmethod
    @UserBlueprint.route('/user/', methods=['GET', 'POST'])
    @login_required
    def user():
        user = db.session.query(User).filter(User.id == current_user.id).first()
        timenow = datetime.datetime.now()
        my_pasts = db.session.query(Pastes) \
            .filter(Pastes.user_id == current_user.id, Pastes.date_timelive >= timenow) \
            .order_by(Pastes.id.desc()).limit(10)

        avatar = user.photo
        return render_template('user.html', user=user, last_pasts=last_pasts(), my_pasts=my_pasts)

    @staticmethod
    @UserBlueprint.route('/edit_profile/', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        update_data = {}

        form = EditProfileForm()
        if form.validate_on_submit():
            for key in form.data:
                if key == 'photo' and form.data[key]:
                    f = form.photo.data
                    filename = str(uuid.uuid4()) + '.' + f.filename.rsplit('.', 1)[1].lower()
                    f.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                    update_data[key] = filename
                    continue
                elif form.data[key] != '' and key != 'submit' and key != 'photo':
                    update_data[key] = form.data[key]
            try:
                query = db.session.query(User) \
                    .filter(User.id == current_user.id) \
                    .update(update_data, synchronize_session='evaluate')
                db.session.flush()
                db.session.commit()
            except:
                pass

            return redirect(url_for('User.user'))

        return render_template('edit_profile.html', form=form)
