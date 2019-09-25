from flask import Flask, session, redirect
from flask_restplus import Api
from random import choice
import os

import toml

from page import Page
from conf.secrets import session_key

from api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
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
    session['gains'].append({'name': game_name, 'privacy': 0, 'time': 0})

    total_game_list = {c['name']: Page(c) for c in config['games']}
    game = total_game_list[game_name]

    return game.content


@app.route('/start')
def start():
    session['game_list'] = [c['name'] for c in config['games']]
    session['privacy'] = 0
    session['time'] = 0
    session['gains'] = []
    page = Page(config['start'])

    session['gains'].append({'name': 'start', 'privacy': 0, 'time': 0})

    return page.content


@app.route('/end')
def end():
    page = Page(config['end'])
    session['gains'].append({'name': 'end', 'privacy': 0, 'time': 0})
    return page.content

