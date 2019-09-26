# TODO:
# - refactoring : game update sessions themself
# - refactoring : remove function that do only one thing
# - refactoring : separate config from init
# - ¿ refactoring : merge some objects with api ?
# - use Score objets for each score

from collections import OrderedDict
from flask import session, redirect, Blueprint, current_app
import toml

game = Blueprint('game', __name__)


@game.route('/')
def main():
    pbn = PetiteBoiteNoire()
    return pbn.next()


@game.route('/restart')
def start():
    pbn = PetiteBoiteNoire(restart=True)
    return pbn.next()


with open('conf/config.toml') as f:
    config = toml.load(f)


class PetiteBoiteNoire(OrderedDict):

    def __init__(self,
                 restart=False,
                 max_time=100,
                 max_privacy=100):

        self.max_time = max_time
        self.max_privacy = max_privacy

        super().__init__(self._games(restart))
        current_app.logger.debug(("Game initialised with game list {}"
                                  .format(self)))

    def _games(self, restart=False):
        games = [c['name'] for c in config['games']]
        if (session
            and 'current' in session
            and session['current'] == games[-1]):
            restart = True

        if not session or restart:
            n = len(games)

            game_dict = {g: Game(name=g,
                                 max_time=self.max_time/n,
                                 max_privacy=self.max_privacy/n)
                         for g in games}
            current_app.logger.debug(game_dict)
            session['game_list'] = [game.dict() for game in game_dict.values()]

        else:
            game_dict = {game['name']: Game(**game)
                         for game in session['game_list']}

        return game_dict

    def next(self):
        games = list(self.keys())
        if 'current' not in session or session['current'] == games[-1]:
            session['current'] = games[0]
        else:
            current = session['current']
            session['current'] = games[games.index(current) + 1]
        return self.current().page

    def current(self):
        current = session['current']
        return self[current]

    def add_gain(self, privacy, time):
        self.current().add_gain(privacy=privacy, time=time)
        # TODO: find a more elegant solution
        self._update_session()

    def gain(self):
        return self.current().gain()

    def gains(self):
        game_list = list(self.keys())
        current_name = self.current().name
        future_games = game_list[game_list.index(current_name) + 1:]

        return [{'name': name, **game.gain()}
                for name, game in self.items()
                if name not in future_games]

    def score(self):
        return self.current().score()

    def scores(self):
        game_list = list(self.keys())
        current_name = self.current().name
        future_games = game_list[game_list.index(current_name) + 1:]

        return [{'name': name, **game.score()}
                for name, game in self.items()
                if name not in future_games]

    def name(self):
        return self.current().name

    def _update_session(self):
        session['game_list'] = [game.dict() for game in self.values()]


class Game():
    name = None
    privacy = None
    time = None
    page = None

    def __init__(self,
                 name,
                 max_privacy=None,
                 max_time=None,
                 privacy=None,
                 time=None):
        self.name = name

        self.max_privacy = max_privacy
        self.privacy = privacy if privacy is not None else max_privacy

        self.max_time = max_time
        self.time = time if time is not None else max_time

        self._get_config()

    def _get_config(self):
        games = {c['name']: c for c in config['games']}
        game_config = games[self.name]

        self.page = page(game_config)

    def dict(self):
        return {'name': self.name,
                'privacy': self.privacy,
                'max_privacy': self.max_privacy,
                'time': self.time,
                'max_time': self.max_time}

    def __str__(self):
        if self.max_privacy or self.max_time:
            return ("name:{}, time:{}, privacy:{}, max_time:{}, max_privacy:{}"
                    .format(self.name,
                            self.time,
                            self.privacy,
                            self.max_time,
                            self.max_privacy))
        return ("name: {}, time:{}, privacy:{}"
                .format(self.name, self.time, self.privacy))

    def __repr__(self):
        return "Game({})".format(str(self))

    def add_gain(self, privacy=0, time=0):
        self.privacy = max(self.privacy + privacy, 0)
        if self.max_privacy:
            self.privacy = min(self.max_privacy, self.privacy)

        self.time = max(self.time + time, 0)
        if self.max_time:
            self.time = min(self.max_time, self.time)

    def gain(self):
        time = self.max_time - self.time if self.max_time else self.time
        privacy = (self.max_privacy - self.privacy
                   if self.max_privacy else self.privacy)
        return {'time': time, 'privacy': privacy}

    def score(self):
        return {'time': self.time, 'privacy': self.privacy}
