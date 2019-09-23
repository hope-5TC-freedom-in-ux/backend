from flask import redirect

class Page():

    def __init__(self, config):
        if 'content' in config:
            self.content = config['content']
        else:
            self.content = redirect(config['url'])

        self.name = config['name'] if 'name' in config else None
