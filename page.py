from flask import redirect


def page(config):
    if 'content' in config:
        page = config['content']
    else:
        page = redirect(config['url'])

    return page
