from pastebin.make_app import make_app, db

from celery import Celery
from celery.task import periodic_task

from datetime import timedelta, datetime
from pastebin.models.models import Pastes

flask_app = make_app()
celery = Celery(__name__, backend=flask_app.config['CELERY_RESULT_BACKEND'],
                broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)


@periodic_task(run_every=timedelta(minutes=10))
def updateDb():
    with flask_app.app_context():
        datenow = datetime.now()
        db.session.query(Pastes).filter(Pastes.date_timelive < datenow).delete()
        db.session.commit()
