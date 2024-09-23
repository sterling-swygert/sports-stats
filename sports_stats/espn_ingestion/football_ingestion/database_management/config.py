import json
import logging
import os

from sports_stats.utils import util


project_root = util.get_project_root()

with open(project_root.joinpath('secrets/pg_creds.json')) as f:
    secrets = json.load(f)


class VariableNotFoundError(Exception):
    pass


class Config(object):
    def __init__(self):
        pass


class LocalConfig(Config):
    def __init__(self):
        super().__init__()
        self.host = 'localhost'
        self.username = secrets.get('username')
        self.password = secrets.get('password')


config_map = {'local': LocalConfig()}


try:
    env = os.environ['ENV']
except KeyError:
    raise VariableNotFoundError('Environment variable "ENV" not set. Please set to proceed.')

try:
    conf = config_map[env]
except KeyError:
    raise KeyError(f'Environment variable "ENV" must be one of: {f", ".join(config_map.keys())}')
