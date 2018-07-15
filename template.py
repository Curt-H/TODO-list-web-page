from jinja2 import Environment, FileSystemLoader
import os

from util import log


def initialize_env():
    # templates path generate
    path = os.path.join(os.path.dirname(__file__), 'templates')
    log(f'template path: {path}')
    # generate loader to load template
    loader = FileSystemLoader(path)
    # create a env
    env = Environment(loader=loader)
    return env


class Template(object):
    e = initialize_env()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        template = cls.e.get_template(filename)
        return template.render(*args, **kwargs)
