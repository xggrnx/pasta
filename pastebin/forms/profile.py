from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField


class EditProfileForm(FlaskForm):
    name = StringField('Real name')
    photo = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    api_key = StringField('Api key')
    submit = SubmitField('Submit')
