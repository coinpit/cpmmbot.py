#!/usr/bin/env python
from pymmbot import mmbot
from pymmbot.utils import common_util

bot = mmbot.MMBot()
bot.connect_coinpit()
bot.connect_bitmex()
common_util.loop()
