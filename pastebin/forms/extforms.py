from flask_security.forms import RegisterForm, Required, StringField, HiddenField
import uuid

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [Required()])
    api_key = HiddenField('api_key')

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.api_key.data = uuid.uuid4().hex