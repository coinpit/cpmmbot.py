import json
from  easydict import EasyDict as edict
import pymmbot.bot_settings as baseSettings
from os import path
import logging.config
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Market maker bot for Coinpit with hedging supported at Bitmex')
    parser.add_argument('--bitmex', '-b', dest='bitmex_apikey_file', required=True,
                        help='Bitmex API KEY json file. example content: \n'
                             '{'
                             '  "ID": "Ag-_DuBvWrO8IK-6FnGhldzR",   '
                             '  "Secret": "_Dss0iITNH5-4QlCNYxqXQ7kA2ngSmhKX4tlRBdn4mmsR3_A" '
                             '}')

    parser.add_argument('--coinpit', '-c', dest='coinpit_apikey_file', required=True,
                        help='api-key downloaded from coinpit. provide path.')

    parser.add_argument('--bh', dest='bitmex_host', help='bitmex host. ex. https://live.coinpit.io/api/v1')
    parser.add_argument('--ch', dest='coinpit_host', help='coinpit host. ex. https://www.bitmex.com/api/v1/')
    args = parser.parse_args()
    return args


def get_settings():
    _settings = {}
    _settings.update(vars(baseSettings))
    return edict(_settings)


def update_api_key(args, _settings):
    with open(args.coinpit_apikey_file) as API_STRING:
        _settings.COINPIT_API_KEY = json.load(API_STRING)

    with open(args.bitmex_apikey_file) as API_STRING:
        as_json = json.load(API_STRING)
        _settings.BITMEX_API_KEY = as_json['ID']
        _settings.BITMEX_API_SECRET = as_json['Secret']


def update_url(args, _settings):
    network = 'livenet' if _settings.COINPIT_API_KEY['userid'][0] == '1' else 'testnet'

    if args.coinpit_host is not None:
        _settings.COINPIT_URL = args.coinpit_host
    else:
        _settings.COINPIT_URL = {"livenet": "https://live.coinpit.io/api/v1",
                                "testnet": "https://live.coinpit.me/api/v1"}[network]

    if args.bitmex_host is not None:
        _settings.BITMEX_URL = args.bitmex_host
    else:
        _settings.BITMEX_URL = {"livenet": "https://www.bitmex.com/api/v1/",
                               "testnet": "https://testnet.bitmex.com/api/v1/"}[network]


def update_logger():
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(log_file_path)

def validate_settings(_settings):
    assert settings.INTEREST_RATE > 0, 'INTEREST_RATE must be greater than 0'
    assert settings.COINPIT_TICK_SIZE >= 1, 'COINPIT_TICK_SIZE must be a number greater than 0'
    assert settings.COINPIT_QTY > 0, 'COINPIT_QTY must be a positive number'
    assert settings.QUANTITY_MULTIPLIER > 0, 'QUANTITY_MULTIPLIER must be greater than 0'
    assert settings.COINPIT_LATCH >= 0.02, 'COINPIT_LATCH should be grater than or equal to 0.02'
    assert settings.HEDGE_INTERVAL > 0, 'HEDGE_INTERVAL must be a positive time in seconds'


settings = get_settings()
args = get_args()
update_api_key(args, settings)
update_url(args, settings)
validate_settings(settings)
update_logger()

print("#### bitmex", settings.BITMEX_URL)
print("#### coinpit", settings.COINPIT_URL)
