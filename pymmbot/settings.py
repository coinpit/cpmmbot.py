import json
from  easydict import EasyDict as edict
import pymmbot.bot_settings as baseSettings
from os import path
import logging.config
import argparse

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

settings = {}
settings.update(vars(baseSettings))
settings = edict(settings)

with open(args.coinpit_apikey_file) as API_STRING:
    settings.COINPIT_API_KEY = json.load(API_STRING)

with open(args.bitmex_apikey_file) as API_STRING:
    as_json = json.load(API_STRING)
    settings.BITMEX_API_KEY = as_json['ID']
    settings.BITMEX_API_SECRET = as_json['Secret']

network = 'livenet' if settings.COINPIT_API_KEY['userid'][0] == '1' else 'testnet'

if args.coinpit_host is not None:
    settings.COINPIT_URL = args.coinpit_host
else:
    settings.COINPIT_URL = {"livenet": "https://live.coinpit.io/api/v1",
                            "testnet": "https://live.coinpit.me/api/v1"}[network]

if args.bitmex_host is not None:
    settings.BITMEX_URL = args.bitmex_host
else:
    settings.BITMEX_URL = {"livenet": "https://www.bitmex.com/api/v1/",
                           "testnet": "https://testnet.bitmex.com/api/v1/"}[network]

print("#### bitmex", settings.BITMEX_URL)
print("#### coinpit", settings.COINPIT_URL)
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
