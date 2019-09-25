# TODO:
# - BREAKING : score and gain return total gain/score
# - BREAKING : change namespaces : don't use same namespace
#    - ¿ <game:game_name> : game with game name
#    - ¿ <game:current> : current game
#    - ¿ <game> : global
# - change api root to /api instead of /api/v0.1 (for swagger), and use
#   namespaces

from flask import session, request, Blueprint
from flask_restplus import Api, Resource, fields, errors

from game import PetiteBoiteNoire

api_version = 'v0.1'
blueprint = Blueprint('api', __name__, url_prefix='/api/' + api_version)
api = Api(blueprint,
          version=api_version,
          title='API La petite boite noire',
          description='API for building games for "La petite boite noire"')


@api.route('/user')
class User(Resource):
    def get(self):
        if 'username' not in session:
            return errors.abort(400, "Username not found. Has it been set ?")
        return {'username': session['username']}

    def put(self):
        if 'username' not in request.form:
            return errors.abort(400, "'username' field not found in sent data")
        session['username'] = request.form['username']
        return {'username': session['username']}


@api.route('/score')
class Score(Resource):

    pbn = None

    def __init__(self, *args, **kwargs):
        self.pbn = PetiteBoiteNoire()
        super().__init__(*args, **kwargs)

    def get(self):
        return self.pbn.score()

    def patch(self):
        privacy = float(request.form['privacy'])
        time = float(request.form['time'])

        self.pbn.add_gain(privacy=privacy, time=time)
        return self.pbn.score()


@api.route('/scores')
class Scores(Resource):

    def get(self):
        pbn = PetiteBoiteNoire()
        return pbn.scores()


@api.route('/gain')
class Gain(Resource):
    def get(self):
        pbn = PetiteBoiteNoire()
        return pbn.gain()


@api.route('/gains')
class Gains(Resource):
    def get(self):
        pbn = PetiteBoiteNoire()
        return pbn.gains()


@api.route('/name')
class Name(Resource):
    def get(self):
        pbn = PetiteBoiteNoire()
        return pbn.name()
