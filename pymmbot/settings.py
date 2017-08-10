import json
from  easydict import EasyDict as edict
import pymmbot.bot_settings as baseSettings
from os import path
import logging.config

settings = {}
settings.update(vars(baseSettings))
settings = edict(settings)

with open(settings.COINPIT_API_FILE) as API_STRING:
    settings.COINPIT_API_KEY = json.load(API_STRING)

with open(settings.BITMEX_API_FILE) as API_STRING:
    as_json = json.load(API_STRING)
    settings.BITMEX_API_KEY = as_json['ID']
    settings.BITMEX_API_SECRET = as_json['Secret']

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
