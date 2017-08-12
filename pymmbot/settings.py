import logging.config
import settings as baseSettings
from os import path
from  easydict import EasyDict as edict


def get_settings():
    _settings = {}
    _settings.update(vars(baseSettings))
    _settings['BITMEX_TOPICS'] = ["instrument", "orderBook10", "order", "execution", "position"]
    return edict(_settings)


def update_url(_settings):
    network = 'livenet' if _settings.COINPIT_API_KEY['userid'][0] == '1' else 'testnet'

    if 'COINPIT_URL' not in _settings:
        _settings.COINPIT_URL = {"livenet": "https://live.coinpit.io/api/v1",
                                 "testnet": "https://live.coinpit.me/api/v1"}[network]

    if 'BITMEX_URL' not in _settings:
        _settings.BITMEX_URL = {"livenet": "https://www.bitmex.com/api/v1/",
                                "testnet": "https://testnet.bitmex.com/api/v1/"}[network]


def update_logger():
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(log_file_path)


def validate_settings(_settings):
    assert _settings.INTEREST_RATE > 0, 'INTEREST_RATE must be greater than 0'
    assert _settings.COINPIT_TICK_SIZE >= 1, 'COINPIT_TICK_SIZE must be a number greater than 0'
    assert _settings.COINPIT_QTY > 0, 'COINPIT_QTY must be a positive number'
    assert _settings.QUANTITY_MULTIPLIER > 0, 'QUANTITY_MULTIPLIER must be greater than 0'
    assert _settings.COINPIT_LATCH >= 0.02, 'COINPIT_LATCH should be grater than or equal to 0.02'
    assert _settings.HEDGE_INTERVAL > 0, 'HEDGE_INTERVAL must be a positive time in seconds'
    assert isinstance(_settings.BITMEX_API_KEY, str), 'Bitmex api key must be a string.'
    assert isinstance(_settings.BITMEX_API_SECRET, str), 'Bitmex secret must be a string.'


settings = get_settings()
update_url(settings)
validate_settings(settings)
update_logger()

print("#### bitmex", settings.BITMEX_URL)
print("#### coinpit", settings.COINPIT_URL)
