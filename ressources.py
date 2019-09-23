from flask import session, request
from flask_restful import Resource, Api

class User(Resource):
    def get(self):
        return {'username': session['username']}

    def put(self):
        session['username'] = request.form['username']
        return {'username': session['username']}

class Score(Resource):
    def get(self):
        return {'privacy': session['privacy'], 'time': session['time']}

    def patch(self):
        session['privacy'] += float(request.form['privacy'])
        session['time'] += float(request.form['time'])
        return {'privacy': session['privacy'], 'time': session['time']}
