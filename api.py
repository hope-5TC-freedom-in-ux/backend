from flask import session, request, Blueprint
from flask_restplus import Api, Resource, fields

api_version = 'v0.1'
blueprint = Blueprint('api', __name__, url_prefix='/api/' + api_version)
api = Api(blueprint,
          version=api_version,
          title='API La petite boite noire',
          description='API for building games for "La petite boite noire"')



@api.route('/user')
class User(Resource):
    def get(self):
        return {'username': session['username']}

    def put(self):
        session['username'] = request.form['username']
        return {'username': session['username']}

@api.route('/score')
class Score(Resource):
    def get(self):
        return {'privacy': session['privacy'], 'time': session['time']}

    def patch(self):
        privacy = float(request.form['privacy'])
        time = float(request.form['time'])

        session['privacy'] += privacy
        session['time'] += time

        session['gains'][-1]['privacy'] += privacy
        session['gains'][-1]['time'] += time

        return {'privacy': session['privacy'], 'time': session['time']}

@api.route('/gains')
class Gains(Resource):
    def get(self):
        return session['gains']
