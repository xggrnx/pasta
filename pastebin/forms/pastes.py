from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

from pastebin.models import db
from pastebin.models.models import Codelanguages
from datetime import timedelta, datetime
from enum import Enum


class LiveTime(Enum):
    N = (timedelta(days=+999999), 'Never')
    M10 = (timedelta(seconds=+600), '10 Minutes')
    H1 = (timedelta(seconds=+3600), '1 Hour')
    D1 = (timedelta(days=+1), '1 Day')
    W1 = (timedelta(days=+7), '1 Week')
    W2 = (timedelta(days=+14), '2 Weeks')
    M1 = (timedelta(days=+30), '1 Month')
    M6 = (timedelta(days=+180), '6 Months')
    Y1 = (timedelta(days=+365), '1 Year')


class PastesForm(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Title"})
    is_private = BooleanField('Private')
    date_timelive = SelectField(
        'Paste Expiration',
        choices=[(i.name, i.value[1]) for i in LiveTime]  # Choises keys and description from LIVE TIME
    )
    paste = TextAreaField('', validators=[DataRequired()], render_kw={"placeholder": "Code"})
    code_id = SelectField('Code', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self):
        super(PastesForm, self).__init__()
        query = Codelanguages.query.order_by(Codelanguages.id).all()
        ctx = [(s.id, s.name) for s in query]
        self.code_id.choices = ctx


class PastesFormGet(FlaskForm):
    title = StringField('Title', render_kw={"placeholder": "Title"})
    is_private = BooleanField('Private')
    code_id = SelectField('Code', coerce=int)
    submit = SubmitField('Search')

    def __init__(self):
        super(PastesFormGet, self).__init__()
        query = Codelanguages.query.order_by(Codelanguages.id).all()
        ctx = [(s.id, s.name) for s in query]
        self.code_id.choices = ctx


def getLifeTime(curr="N"):
    return datetime.now() + LiveTime[curr].value[0]
