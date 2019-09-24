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
        privacy = float(request.form['privacy'])
        time = float(request.form['time'])

        session['privacy'] += privacy
        session['time'] += time

        session['gains'][-1]['privacy'] += privacy
        session['gains'][-1]['time'] += time

        return {'privacy': session['privacy'], 'time': session['time']}

class Gains(Resource):
    def get(self):
        return session['gains']
