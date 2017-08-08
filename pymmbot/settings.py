from  easydict import EasyDict as edict
import bot_settings as baseSettings
import user_settings.user as userSettings
from os import path
import logging.config
import sys
import os
import importlib

def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    file_names = os.listdir(fullpath)
    for file_name in file_names:
        filename, ext = os.path.splitext(file_name)
        if ext == '.py':
            user_module = importlib.import_module(fullpath, filename)
            importlib.reload(user_module)
            settings.update(vars(user_module))


settings = {}
settings.update(vars(baseSettings))
settings.update(vars(userSettings))
# import_path(os.path.join('..', 'pymmbot', 'settings'))

settings = edict(settings)

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)


