#!/usr/bin/env python
from pymmbot import mmbot
from pymmbot.utils import common_util

bot = mmbot.MMBot()
bot.connect()
# bot.initiate()
common_util.loop()
