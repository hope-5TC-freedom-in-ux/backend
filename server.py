from flask import Flask, session, redirect
from flask_restful import Api
from random import choice
import os

import toml

from ressources import Score, User
from page import Page
from conf.secrets import session_key

app = Flask(__name__)
api = Api(app)

app.secret_key = session_key

with open('conf/config.toml') as f:
    config = toml.load(f)


@app.route('/')
def main():
    if not session:
        return redirect('/start')
    return redirect('/game')


@app.route('/game')
def game():
    game_list = session['game_list']

    if not game_list:
        return redirect('/end')

    game_name = game_list.pop(0)
    session['game_list'] = game_list

    total_game_list = {c['name']: Page(c) for c in config['games']}
    game = total_game_list[game_name]

    return game.content


@app.route('/start')
def start():
    session['game_list'] = [c['name'] for c in config['games']]
    session['privacy'] = 0
    session['time'] = 0
    page = Page(config['start'])
    return page.content


@app.route('/end')
def end():
    page = Page(config['end'])
    return page.content

api_version = 'v0.1'
api.add_resource(User, '/api/' + api_version + '/user')
api.add_resource(Score, '/api/' + api_version + '/score')
