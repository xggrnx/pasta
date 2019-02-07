from flask import Blueprint, url_for, request, jsonify, make_response, current_app
from pastebin.models.models import Pastes, User
from pastebin.models import db
import uuid, datetime
from pastebin.forms.pastes import getLifeTime

ApiBlueprint = Blueprint('Api', __name__, url_prefix='/api')


class ApiKey(object):
    @staticmethod
    @ApiBlueprint.route('/v1/add', methods=['GET', 'POST'])
    def create_paste():
        if not request.json or not 'api_key' in request.json:
            return make_response(jsonify({'error': 'Wrong api key or request type'}), 404)
        try:
            user_query = db.session.query(User).filter(User.api_key == request.json['api_key']).one()

            request_paste = Pastes()

            request_paste.title = request.json.get('title', 'Untitled')
            request_paste.link = uuid.uuid4().hex
            request_paste.paste = request.json.get('paste')
            request_paste.date = datetime.datetime.now()

            request_paste.date_timelive = getLifeTime(
                curr=(request.json.get('date_timelive', 'H1')))  # Enum LiveTime in pastes
            request_paste.private = bool(request.json.get('is_private', 'False'))  # check private
            request_paste.user_id = user_query.id
            request_paste.code_id = request.json.get('code_id', '1')  # code lang id - deafault id 1 is None

            db.session.add(request_paste)
            db.session.flush()
            db.session.commit()

            return make_response(
                jsonify({'link': '{0}{1}'.format(
                    current_app.config.get('DOMAIN'), url_for('Index.pastes', link=request_paste.link))}), 200
            )

        except:
            return make_response(jsonify({'error': 'Wrong request'}), 500)


"""
/api/v1/add  # path
{
	"api_key": "53eea1f67802407a8a57303361586636", #required
	"paste": "<h1>Hello wrold!</h1>", #required
}

"""
